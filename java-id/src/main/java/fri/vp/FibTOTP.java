package fri.vp;

import java.util.HexFormat;

import static fri.vp.OTP.generateTOTPSHA256;

public class FibTOTP {
    public static void main(String[] args) {
        // Uporabite spodnji ključ
        final byte[] key = HexFormat.of().parseHex("581f22628ce7b73da43abfceb41c94a5");

        // Implementirajte program, ki vrača enkratna gesla izračunana iz časa
        // Lahko uporabite funkcijo System.currentTimeMillis(), a časovno vrednost
        // ustrezno popravite, da bo vsebovala sekunde
        // interval naj bo dolg 30 sekund, geslo pa 6 mest
        // Izpišite ga na standardni zaslon
        final long time = System.currentTimeMillis() / 1000;
        final String otp = generateTOTPSHA256(key, time, 30, 6);
        System.out.println(otp);
    }
}