package fri.vp;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Scanner;

import static fri.vp.OTP.generateResponseHMAC256;

public class FibChallengeResponse {
    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        // Ključ
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        // S standardnega vhoda preberite poziv (to bo 6-mestno število)
        // izračunajte odziv s pomočjo ustrezne funkcije v razredu OTP
        // odziv izpišite na standardni izhod

    }
}