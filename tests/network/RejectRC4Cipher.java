import javax.net.ssl.*;

public class RejectRC4Cipher {
    public static void main(String[] args) {
        try {
            SSLContext context = SSLContext.getInstance("TLS", "BCJSSE");
            context.init(null, null, null);
            SSLSocketFactory factory = context.getSocketFactory();
            try (SSLSocket socket = (SSLSocket) factory.createSocket("google.com", 443)) {
                socket.setEnabledCipherSuites(new String[] { "TLS_RSA_WITH_RC4_128_SHA" });
                socket.startHandshake();
                System.out.println("RESULT_DANGER_RC4_ALLOWED");
                System.exit(0);
            }
        } catch (Exception e) {
            System.out.println("RESULT_SUCCESS_FIPS_ENFORCED");
            System.exit(1);
        }
    }
}