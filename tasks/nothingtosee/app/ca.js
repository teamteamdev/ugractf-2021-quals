#!/usr/bin/env node

const crypto = require('crypto');
const forge = require('node-forge');
const fs = require('fs');
const path = require('path');

const keys = forge.rsa.generateKeyPair(2048);
const cert = forge.pki.createCertificate();
cert.publicKey = keys.publicKey;
cert.validity.notBefore = new Date('2021-02-26T08:37:00Z');
cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 10);
cert.serialNumber = Math.floor(Math.random() * 281474976711000).toString(16).padStart(14, '0');
const attrs = [
    {shortName: 'C', value: 'RU'},
    {shortName: 'ST', value: 'Ugra'},
    {shortName: 'L', value: 'Khanty-Mansiysk'},
    {shortName: 'O', value: '[team Team]'},
    {shortName: 'OU', value: 'NOC'},
    {shortName: 'CN', value: '[team Team] Certificate Authority'}
];
cert.setSubject(attrs);
cert.setIssuer(attrs);
cert.setExtensions([
    {name: 'basicConstraints', cA: true},
    {name: 'keyUsage', keyCertSign: true, keyEncipherment: true},
    {name: 'extKeyUsage', serverAuth: true},
    {name: 'nsCertType', server: true, sslCA: true}
])
cert.sign(keys.privateKey, forge.md.sha512.create());

const certPem = forge.pki.certificateToPem(cert);
const keyPem = forge.pki.privateKeyToPem(keys.privateKey);

fs.writeFileSync('root.key', keyPem);
fs.writeFileSync('root.crt', certPem);
