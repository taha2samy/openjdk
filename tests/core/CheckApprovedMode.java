public class CheckApprovedMode {
    public static void main(String[] args) {
        String fipsProp = System.getProperty("org.bouncycastle.fips.approved_only");
        if ("true".equals(fipsProp)) {
            System.out.println("[PASS] JVM Property for STRICT FIPS Mode is SET to TRUE.");
            System.exit(0);
        } else {
            System.err.println("[FAIL] JVM Property is NOT set! BCFIPS will run in General Mode.");
            System.exit(1);
        }
    }
}