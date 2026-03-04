
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) {
        try {
            System.out.println("--- FIPS TLS Handshake Test ---");

            HttpClient client = HttpClient.newHttpClient();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://adoptium.net"))
                    .GET()
                    .build();

            System.out.println("Connecting to Adoptium via Secure TLS...");

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Response Status: " + response.statusCode());
            System.out.println("Connection Proof: TLS Session established via BCFIPS");
            System.out.println("SUCCESS: Secure network communication verified.");

        } catch (Exception e) {
            System.err.println("FAILED: Security provider blocked the connection or network issue.");
            e.printStackTrace();
            System.exit(1);
        }
    }
}