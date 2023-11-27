package fri.vp;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Scanner;

import static fri.vp.OTP.generateResponseHMAC256;

public class FibChallengeResponse {
    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        System.out.print("Enter OTP challenge: ");

        final Scanner sc = new Scanner(System.in);
        final String challenge = sc.nextLine();

        System.out.println(generateResponseHMAC256(key, challenge));
    }
}