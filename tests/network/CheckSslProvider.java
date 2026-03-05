import javax.net.ssl.SSLContext;

public class CheckSslProvider {
    public static void main(String[] args) {
        try {
            SSLContext context = SSLContext.getDefault();
            String providerName = context.getProvider().getName();

            System.out.println("Current SSL Provider: " + providerName);

            if ("BCJSSE".equals(providerName)) {
                System.out.println("RESULT_SUCCESS_PROVIDER_VERIFIED");
                System.exit(0);
            } else {
                System.out.println("RESULT_FAIL_WRONG_PROVIDER");
                System.exit(1);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}