import javax.net.ssl.*;
import java.net.URL;
import java.security.*;
import java.util.Enumeration;

public class Main {
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("   FIPS 140-3 NETWORK DIAGNOSTICS      ");
        System.out.println("========================================");

        try {
            System.out.println("[INFO] Security Providers Priority:");
            Provider[] providers = Security.getProviders();
            for (int i = 0; i < Math.min(providers.length, 5); i++) {
                System.out.println(
                        "   " + (i + 1) + ". " + providers[i].getName() + " (v" + providers[i].getVersion() + ")");
            }

            String tsPath = System.getProperty("javax.net.ssl.trustStore");
            String tsType = System.getProperty("javax.net.ssl.trustStoreType");
            String tsPass = System.getProperty("javax.net.ssl.trustStorePassword");

            System.out.println("[INFO] TrustStore Path: " + tsPath);
            System.out.println("[INFO] TrustStore Type: " + tsType);

            if (tsPath != null) {
                KeyStore ks = KeyStore.getInstance(tsType != null ? tsType : KeyStore.getDefaultType());
                java.io.FileInputStream fis = new java.io.FileInputStream(tsPath);
                ks.load(fis, tsPass != null ? tsPass.toCharArray() : null);
                fis.close();

                int certCount = 0;
                Enumeration<String> aliases = ks.aliases();
                while (aliases.hasMoreElements()) {
                    aliases.nextElement();
                    certCount++;
                }
                System.out.println("[INFO] Certificates found in TrustStore: " + certCount);
            }

            System.out.println("[INFO] SSLContext Protocol: " + SSLContext.getDefault().getProtocol());

            String testUrl = "https://www.facebook.com";
            System.out.println("[INFO] Attempting HTTPS connection to: " + testUrl);

            URL url = new URL(testUrl);
            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
            connection.setConnectTimeout(10000);
            connection.setReadTimeout(10000);

            long startTime = System.currentTimeMillis();
            connection.connect();
            long endTime = System.currentTimeMillis();

            System.out.println("[SUCCESS] Connection established in " + (endTime - startTime) + "ms");
            System.out.println("[SUCCESS] HTTP Response Code: " + connection.getResponseCode());

        } catch (Throwable t) {
            System.err.println("[FAILED] Error: " + t.getMessage());

            Throwable cause = t.getCause();
            while (cause != null) {
                System.err.println("[FAILED] Caused by: " + cause.toString());
                cause = cause.getCause();
            }

            System.err.println("\n[DEBUG] Stack Trace:");
            t.printStackTrace();
            System.exit(1);
        }
        System.out.println("========================================");
    }
}