package fri.vp;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

import static fri.vp.OTP.generateHOTPSHA1;

public class FibHOTP {

    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        for (int i = 0; i < 10; i++) {
            final String otp = generateHOTPSHA1(key, i, 6);
            System.out.println(i + " " + otp);
        }
    }
}