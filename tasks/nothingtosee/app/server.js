#!/usr/bin/env node

const https = require('https');
const crypto = require('crypto');
const forge = require('node-forge').pki;
const fs = require('fs');
const path = require('path');
const tls = require('tls');

const STATE_DIR = process.argv[2] ? process.argv[2] : __dirname
const PREFIX = 'ugra_v1_p0sm0tr3l1_';
const SECRET2 = Buffer.from('810adD012KSDAl10');
const SALT2_SIZE = 12;

const generateDefaultCert = () => {
    return generateCert(undefined, true);
}

const generateCert = (token, isDefault) => {
    const certPath = path.join(STATE_DIR, isDefault ? 'default.cert' : token + '.cert');
    const keyPath = path.join(STATE_DIR, isDefault ? 'default.key' : token + '.key');

    const flag = isDefault ? ''
        : PREFIX + crypto.createHmac('sha256', SECRET2).update(Buffer.from(token)).digest('hex').slice(0, SALT2_SIZE);

    if (fs.existsSync(certPath) && fs.existsSync(keyPath))
        return { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) };

    const keys = forge.rsa.generateKeyPair(1024);
    const cert = forge.createCertificate();
    cert.publicKey = keys.publicKey;
    cert.validity.notBefore = new Date();
    cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 10);
    cert.serialNumber = Math.floor(Math.random() * 281474976711000).toString(16)
    const attrs = [{
        shortName: 'C', value: 'RU',
    }, {
        shortName: 'ST', value: 'Ugra',
    }, {
        shortName: 'L', value: 'Khanty-Mansiysk',
    }, {
        shortName: 'O', value: '[team Team]',
    }, {
        shortName: 'OU', value: 'Team',
    }, {
        shortName: 'CN', value: isDefault ? "Flag isn't here." : flag,
    }];
    cert.setSubject(attrs);
    cert.setIssuer(attrs);
    cert.sign(keys.privateKey);

    const certPem = forge.certificateToPem(cert);
    const keyPem = forge.privateKeyToPem(keys.privateKey);

    fs.writeFileSync(certPath, certPem);
    fs.writeFileSync(keyPath, keyPem);

    return { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) };
};

const httpOptions = {
    SNICallback: (hostname, cb) => {
        const cert = generateCert(hostname.split('.')[0]);
        const ctx = tls.createSecureContext(cert);
        cb(null, ctx);
    },
    ...generateDefaultCert()
}

const server = https.createServer(httpOptions, (req, res) => {
    res.end('Nothing to see here. Move along.')
}).listen(31337)
