import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.OutputStream;

public class Tls13Connection {
    public static void main(String[] args) throws Exception {
        SSLContext context = SSLContext.getInstance("TLSv1.3", "BCJSSE");
        context.init(null, null, null);

        SSLSocketFactory factory = context.getSocketFactory();
        try (SSLSocket socket = (SSLSocket) factory.createSocket("google.com", 443)) {
            socket.setEnabledProtocols(new String[] { "TLSv1.3" });
            socket.startHandshake();

            System.out.println("TLS 1.3 Handshake Successful: " + socket.getSession().getProtocol());
            System.exit(0);
        }
    }
}