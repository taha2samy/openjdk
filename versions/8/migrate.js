var BC = new org.bouncycastle.jcajce.provider.BouncyCastleFipsProvider();
java.security.Security.addProvider(BC);

var pemPath = "/tmp/cacert.pem";
var destPath = "/tmp/cacerts.bcfks";
var password = new java.lang.String("changeit").toCharArray();

var destKs = java.security.KeyStore.getInstance("BCFKS", "BCFIPS");
destKs.load(null, null);

var cf = java.security.cert.CertificateFactory.getInstance("X.509");
var fis = new java.io.FileInputStream(pemPath);
var certs = cf.generateCertificates(fis);
var iter = certs.iterator();

var count = 0;
while (iter.hasNext()) {
    var cert = iter.next();
    destKs.setCertificateEntry("cert_" + count, cert);
    count++;
}
fis.close();

var fos = new java.io.FileOutputStream(destPath);
destKs.store(fos, password);
fos.close();

print("SUCCESS: Created BCFKS TrustStore with " + count + " certificates");