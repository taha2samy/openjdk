import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;

public class RejectAnonCipher {
    public static void main(String[] args) {
        try {
            SSLContext context = SSLContext.getInstance("TLS", "BCJSSE");
            context.init(null, null, null);
            SSLSocketFactory factory = context.getSocketFactory();

            try (SSLSocket socket = (SSLSocket) factory.createSocket("google.com", 443)) {
                String[] anonSuites = { "TLS_DH_anon_WITH_AES_128_CBC_SHA" };
                socket.setEnabledCipherSuites(anonSuites);

                socket.startHandshake();

                System.out.println("RESULT_DANGER_ANON_ALLOWED");
                System.exit(0);
            }
        } catch (Exception e) {
            System.out.println("RESULT_SUCCESS_FIPS_ENFORCED");
            System.err.println("Rejection Reason: " + e.getMessage());
            System.exit(1);
        }
    }
}