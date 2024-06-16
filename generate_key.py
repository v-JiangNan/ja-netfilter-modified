import base64

from Crypto.Hash import SHA1, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.asn1 import DerSequence, DerObjectId, DerNull, DerOctetString
from Crypto.Util.number import ceil_div
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# noinspection PyTypeChecker
def pkcs15_encode(msg_hash, emLen, with_hash_parameters=True):
    """
    Implement the ``EMSA-PKCS1-V1_5-ENCODE`` function, as defined
    :param msg_hash: hash object
    :param emLen: int
    :param with_hash_parameters: bool
    :return: An ``emLen`` byte long string that encodes the hash.
    """
    digestAlgo = DerSequence([DerObjectId(msg_hash.oid).encode()])

    if with_hash_parameters:
        digestAlgo.append(DerNull().encode())

    digest = DerOctetString(msg_hash.digest())
    digestInfo = DerSequence([
        digestAlgo.encode(),
        digest.encode()
    ]).encode()

    # We need at least 11 bytes for the remaining data: 3 fixed bytes and
    # at least 8 bytes of padding).
    if emLen < len(digestInfo) + 11:
        raise TypeError("Selected hash algorithm has a too long digest (%d bytes)." % len(digest))
    PS = b'\xFF' * (emLen - len(digestInfo) - 3)
    return b'\x00\x01' + PS + b'\x00' + digestInfo


certBase64 = "MIIFTDCCAzSgAwIBAgIBDTANBgkqhkiG9w0BAQsFADAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBMB4XDTIyMDcyNTIzMTcwOVoXDTMyMDcyMzIzMTcwOVowHzEdMBsGA1UEAwwUcHJvZDJ5LWZyb20tMjAyMDEwMTkwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDDx3gz77KvezmZJhwkF/10Q3vESk96tK6wJ00CSKkLybRDeQVOlHX3QAnPL7BjwCTzHqErsuyPuiZ6YTAVE/n7hLhIbh3lC+EBbxpa2hpIdIvUimr70iSrH9ZBWmnn5Fxy4r/r0tbxr34zpQzu4uWLiEqmOiDfRN+Zzj9FBaJ/gKsuhF7zNAbFHsClYntim5furDRITBra28nu0hfQIEBSHGPS2EKWTbKk2ifBLzMEDp99zIGEe/hrLpgBhdwGVD7VJsoeTXnvcgpt+91kiM918GWThO1L3eKU6W2mGZQv1bRyps7Fo61NElNWtJqqZ3KKyxJGyR1QpdOHd9flAesvYwb/lvc4uqYiKqwvvn+4iHPQlLtZDbzj0ICbKtVKSWgSprh0T5ZQGGNWXN4OMHtg9EuXvbagLshTEDkLKLzEBqSNpNmMmyzwyNO9/voQmHLjiWLdjVIYndjl15G+A9Dw5mVYqzKPMLEpHzg6ldkKJkGAxNBhCMUsmbEypT6r7wsdTvgEwFnP8ToOsAb12lSLxoR2bOT3xJ3WIfbyjvlBnauXfdu6SFF/82QFrLtQyddPvCHEiJTI0NmSYhjQObFohXMVVoXjGbXvuqgJNbc5UK06pCGQ2jKw4j6k1kw2g4fEYBd1fvEzb1/t+izpP8dEI0365xh0C1dpQjUj3uyRywIDAQABo4GZMIGWMEgGA1UdIwRBMD+AFKOetkhnQhI2Qb1t4Lm0oFKLl/GzoRykGjAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBggkA0myxg7KDeeEwCQYDVR0TBAIwADATBgNVHSUEDDAKBggrBgEFBQcDATALBgNVHQ8EBAMCBaAwHQYDVR0OBBYEFCTaESKW9YVBwJNH6DEjTPTAhAL/MA0GCSqGSIb3DQEBCwUAA4ICAQA29wUDKatiQe1S0qfId+1dRWnYznrHE0Cx41HUaeI5hvdZrFbDIP6syb/S9oAXST6w4pfgh80jk1xVL+B7NT5kFC+AI7mpd8dK8Z+K67tagYg41TdLGfSHqK+lljln5ElqUEN21fba5CVZplE286jy973XFOFbWZUpJC/5onCCAh8pK8AqpN7k3ovR6bfAga41UWdTnGeiyw9+XOj30ryebseTKaDfjQxsxEmyuA8YYCu9lgb58cvVrvc99So8KdOBaxHnxeEfiUqvPA8Y0QG7lc5elZYQ6cbiIqqsb/k9XSgB2Gk4CjuacBSxCAfd06NlJvZSDFSR1HTKhQfPLIQY1OpBC+NrKRWnQT4/IORL6F36gI9lTK+ioX8mzQ2bvXn4sXA3jrpRnGM2WemQvMPvstfSDKfcUdKjwX3rZ2jMwREkx/thtF3Huvsc8suOyzto1faD8mV0m4guq85fb4c9ki6cinz3QM2k6otVvh67gK116RZ7I8P/urTWvK7IOdwOE7UVqtpEe6TKvNhr1rzeaxUMdPcD0kY7fhBpuPwEQA+Xk0uiVR+XbpaPD4HWuapJm+31jC7zBp/BamRI25v26P5qMUQF/+P7eE4Ah/X0Rtf2Qvr2+p9kbfqalT8EiqOsvRiTvlMG1hdo33JdcwsxC05BWvZ++7Af0FgJ3TtFlw=="

cert = x509.load_der_x509_certificate(base64.b64decode(certBase64))
public_key = cert.public_key()
sign = int.from_bytes(cert.signature, byteorder="big", )
print(f"sign:{sign}")

modBits = public_key.key_size
digest_cert = SHA256.new(cert.tbs_certificate_bytes)
r = int.from_bytes(pkcs15_encode(digest_cert, ceil_div(modBits, 8)), byteorder='big', signed=False)
print(f"result:{r}")

licenseId = 'ZCB571FZHV'
licensePart = '{"licenseId": "ZCB571FZHV", "licenseeName": "MoYuno", "assigneeName": "", "assigneeEmail": "", "licenseRestriction": "", "checkConcurrentUse": false, "products": [{"code": "PDB", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PSI", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PPC", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PCWMP", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PPS", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PRB", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "II", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": false}, {"code": "PGO", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PSW", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}, {"code": "PWS", "fallbackDate": "2030-12-31", "paidUpTo": "2030-12-31", "extended": true}], "metadata": "0120220701PSAN000005", "hash": "TRIAL:-594988122", "gracePeriodDays": 7, "autoProlongated": false, "isAutoProlongated": false}'

digest = SHA1.new(licensePart.encode('utf-8'))

with open('ca.key') as prifile:
    private_key = RSA.import_key(prifile.read())
    # 使用私钥对HASH值进行签名
    signature = pkcs1_15.new(private_key).sign(digest)

    sig_results = base64.b64encode(signature)
    licensePartBase64 = base64.b64encode(bytes(licensePart.encode('utf-8')))
    public_key.verify(
        base64.b64decode(sig_results),
        base64.b64decode(licensePartBase64),
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA1(),
    )
    result = licenseId + "-" + licensePartBase64.decode('utf-8') + "-" + sig_results.decode('utf-8') + "-" + certBase64
    print(result)
