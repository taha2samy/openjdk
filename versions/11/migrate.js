
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
    var alias = "cert_" + count;
    destKs.setCertificateEntry(alias, cert);
    count++;
}
fis.close();
var fos = new java.io.FileOutputStream(destPath);
destKs.store(fos, password);
fos.close();
print("SUCCESS: Created modern BCFKS TrustStore with " + count + " Root CAs!");
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
    destKs.setCertificateEntry("rootca_" + count, cert);
    count++;
}
fis.close();

var fos = new java.io.FileOutputStream(destPath);
destKs.store(fos, password);
fos.close();

print("SUCCESS: Created modern BCFKS TrustStore with " + count + " Root CAs!");


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
    var alias = "cert_" + count;
    destKs.setCertificateEntry(alias, cert);
    count++;
}
fis.close();
var fos = new java.io.FileOutputStream(destPath);
destKs.store(fos, password);
fos.close();
print("SUCCESS: Created modern BCFKS TrustStore with " + count + " Root CAs!");