package fri.vp;

import java.util.HexFormat;

import static fri.vp.OTP.generateTOTPSHA256;

public class FibTOTP {
    public static void main(String[] args) throws InterruptedException {
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");
        final long time = System.currentTimeMillis() / 1000;
        final String otp = generateTOTPSHA256(key, time, 30, 6);
        System.out.println(otp);
    }
}