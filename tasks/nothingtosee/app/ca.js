#!/usr/bin/env node

const crypto = require('crypto');
const forge = require('node-forge').pki;
const fs = require('fs');
const path = require('path');

const keys = forge.rsa.generateKeyPair(2048);
const cert = forge.createCertificate();
cert.publicKey = keys.publicKey;
cert.validity.notBefore = new Date('2021-02-26T08:37:00Z');
cert.validity.notAfter = new Date(cert.validity.notBefore);
cert.validity.notAfter.setFullYear(cert.validity.notAfter.getFullYear() + 10);
cert.serialNumber = '03133700031337000313370003133701'
const attrs = [
    {shortName: 'C', value: 'RU'},
    {shortName: 'ST', value: 'Ugra'},
    {shortName: 'L', value: 'Khanty-Mansiysk'},
    {shortName: 'O', value: 'team Team'},
    {shortName: 'OU', value: 'NOC'},
    {shortName: 'CN', value: 'team Team Ugra Branch CA'}
];
cert.setSubject(attrs);
cert.setIssuer(attrs);
cert.setExtensions([
    {name: 'basicConstraints', cA: true, critical: true},
    {name: 'keyUsage', keyCertSign: true, keyEncipherment: true, cRLSign: true},
    {name: 'extKeyUsage', serverAuth: true},
    {name: 'nsCertType', server: true, sslCA: true},
    {name: 'subjectKeyIdentifier'}
])
cert.sign(keys.privateKey);

const certPem = forge.certificateToPem(cert);
const keyPem = forge.privateKeyToPem(keys.privateKey);

fs.writeFileSync('root.key', keyPem);
fs.writeFileSync('root.crt', certPem);
