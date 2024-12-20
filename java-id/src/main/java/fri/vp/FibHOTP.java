package fri.vp;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

public class FibHOTP {

    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        // Uporabimo sledeč ključ (je zavoljo preprostopsti implementacije enak za vse uporabnike,
        // v produkciji mora imeti vsak uporabnik svojega)
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        // Ustvarite 10 enkratnih gesel za vrednosti med 0 in 10.
        // Gesla naj bodo 6-mestna, izračunana naj bodo s HMAC-SHA1.
        // Gesla izpišite na standardni izhod
        // Pri prijavi  v spletno aplikacijo morate uporabiti pravilnega
    }
}