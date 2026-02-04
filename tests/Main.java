import javax.net.ssl.HttpsURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        System.out.println("Java is working correctly!");
        try {
            URL url = new URL("https://www.google.com");
            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.connect();
            System.out.println("SSL/Network test passed: Connected to Google.");
        } catch (Exception e) {
            System.err.println("SSL test failed: " + e.getMessage());
            System.exit(1);
        }
    }
}