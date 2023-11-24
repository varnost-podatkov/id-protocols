package fri.vp;

import org.openauthentication.otp.OneTimePasswordAlgorithm;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

import static org.openauthentication.otp.TOTP.generateTOTP256;

public class OTP {

    public static String generateTOTPSHA256(byte[] key, long time, long interval, long digits) {
        final long l = time / interval;
        final StringBuilder timeString = new StringBuilder(Long.toHexString(l).toUpperCase());
        while (timeString.length() < 16) {
            timeString.insert(0, "0");
        }

        return generateTOTP256(HexFormat.of().formatHex(key),
                timeString.toString(),
                String.valueOf(digits));
    }

    public static String generateHOTPSHA1(byte[] key, int value, int digits) throws NoSuchAlgorithmException, InvalidKeyException {
        return OneTimePasswordAlgorithm.generateOTP(key, value, digits, false, 16);
    }

    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        for (int i = 0; i < 10; i++) {
            final String otp = generateHOTPSHA1(key, i, 6);
            System.out.println(i + " " + otp);
        }
    }

    public static void mainTOTP(String[] args) throws InterruptedException {
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");
        final long time = System.currentTimeMillis() / 1000;
        final String otp = generateTOTPSHA256(key, time, 30, 6);
        System.out.println(otp);
    }
}