import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.IOException;

public class RejectWeakTls {
    public static void main(String[] args) {
        try {
            SSLContext context = SSLContext.getInstance("TLS", "BCJSSE");
            context.init(null, null, null);

            SSLSocketFactory factory = context.getSocketFactory();
            try (SSLSocket socket = (SSLSocket) factory.createSocket("google.com", 443)) {
                // Attempt to force TLSv1.0 (Weak Protocol)
                socket.setEnabledProtocols(new String[] { "TLSv1" });
                socket.startHandshake();

                System.out.println("[FAIL] Vulnerability! TLSv1.0 connection allowed.");
                System.exit(0);
            }
        } catch (Exception e) {
            System.out.println("[PASS] Weak TLS connection rejected.");
            System.err.println("Exception: " + e.getMessage());
            System.exit(1);
        }
    }
}