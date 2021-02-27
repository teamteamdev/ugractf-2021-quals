#!/usr/bin/env node

const https = require('https');
const crypto = require('crypto');
const forge = require('node-forge').pki;
const fs = require('fs');
const path = require('path');
const tls = require('tls');

const DOMAIN = 'nothing.q.2021.ugractf.ru';
const BASE_DIR = __dirname;
const STATE_DIR = process.argv[2] ? process.argv[2] : __dirname;
const PREFIX = 'ugra_v1_p0sm0tr3l1_';
const TOKEN_SECRET = Buffer.from("71A4f8fdE203ab7D");
const TOKEN_SALT_SIZE = 16;
const FLAG_SECRET = Buffer.from('810adD012KSDAl10');
const FLAG_SALT_SIZE = 12;

const ROOT_KEY = fs.readFileSync(path.join(BASE_DIR, 'root.key'));
const ROOT_CERT = fs.readFileSync(path.join(BASE_DIR, 'root.crt'))
const DH_PARAM = fs.readFileSync(path.join(BASE_DIR, 'dh.pem'))


const verifyToken = (token) => {
    const realPart = token.slice(0, -TOKEN_SALT_SIZE);
    const hashedPart = token.slice(-TOKEN_SALT_SIZE);
    const expectedHash = crypto
                          .createHmac('sha256', TOKEN_SECRET)
                          .update(Buffer.from(realPart))
                         .digest('hex')
                         .slice(0, TOKEN_SALT_SIZE);
    return hashedPart == expectedHash;
}


const generateCert = (token) => {
    const rootKey = forge.privateKeyFromPem(ROOT_KEY);
    const rootCert = forge.certificateFromPem(ROOT_CERT);

    const certPath = path.join(STATE_DIR, `${token}.crt`);
    const keyPath = path.join(STATE_DIR, `${token}.key`);

    if (fs.existsSync(certPath) && fs.existsSync(keyPath))
        return { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) };

    const keys = forge.rsa.generateKeyPair(2048);
    const cert = forge.createCertificate();
    cert.publicKey = keys.publicKey;
    cert.validity.notBefore = new Date();
    cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 1);
    cert.serialNumber = Math.floor(Math.random() * 281474976711000).toString(16).padStart(14, '0');
    const attrs = [
        {shortName: 'C', value: 'RU'},
        {shortName: 'ST', value: 'Ugra'},
        {shortName: 'L', value: 'Khanty-Mansiysk'},
        {shortName: 'O', value: '[team Team]'},
        {shortName: 'OU', value: 'NOC'},
        {shortName: 'CN', value: token === 'default' ? `localhost` : `${token}.${DOMAIN}`}
    ];
    cert.setSubject(attrs);
    cert.setIssuer(rootCert.issuer.attributes);
    if (token !== 'default') {
        const flag = PREFIX + crypto
                               .createHmac('sha256', FLAG_SECRET)
                               .update(Buffer.from(token))
                               .digest('hex')
                               .slice(0, FLAG_SALT_SIZE);
        cert.setExtensions([
            {name: 'nsComment', comment: flag}
        ]);
    }

    cert.setExtensions([
        {name: 'basicConstraints', cA: false},
        {name: 'keyUsage', digitalSignature: true, keyEncipherment: true, dataEncipherment: true},
        {name: 'extKeyUsage', serverAuth: true},
        {name: 'nsCertType', server: true, sslCA: true, objsign: true, objCA: true},
        {name: 'subjectAltName', altNames: [{
            type: 6,
            value: token === 'default' ? `localhost` : `${token}.${DOMAIN}`
        }]},
        {name: 'subjectKeyIdentifier'}
    ]);
    
    cert.sign(rootKey);

    const certPem = forge.certificateToPem(cert);
    const keyPem = forge.privateKeyToPem(keys.privateKey);

    fs.writeFileSync(certPath, certPem + '\n' + ROOT_CERT);
    fs.writeFileSync(keyPath, keyPem);

    return { key: keyPem, cert: certPem };
};

const secureOptions = {
    ca: ROOT_CERT,
    sigalgs: 'RSA+SHA384',
    dhparam: DH_PARAM,
    minVersion: 'TLSv1.2',
    maxVersion: 'TLSv1.2',
    ciphers: 'ECDHE-RSA-AES256-GCM-SHA384',
    honorCipherOrder: true
};

https.createServer({
    SNICallback: (hostname, cb) => {
        const token = hostname.split('.')[0];
        const cert = (hostname === `${token}.${DOMAIN}` && verifyToken(token)) 
                        ? generateCert(token)
                        : generateCert('default');
        cb(null, tls.createSecureContext({
            ...cert,
            ...secureOptions
        }));
    },
    ...generateCert('default'),
    ...secureOptions
}, (_, res) => {
    res.end('Nothing to see here. Move along.')
}).listen(9443);
