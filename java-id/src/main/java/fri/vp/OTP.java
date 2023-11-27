package fri.vp;

import org.openauthentication.otp.OneTimePasswordAlgorithm;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

import static org.openauthentication.otp.TOTP.generateTOTP256;

public class OTP {

    /**
     * Ustvari enkratno geslo na podlagi časovne vrednosti
     *
     * @param key      ključ
     * @param time     trenuten čas v formatu UNIX
     * @param interval časovni interval
     * @param digits   število znakov
     * @return Enkratno geslo
     */
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

    /**
     * Ustvari enkratno geslo na osnovi funkcije HMAC-SHA1
     *
     * @param key    ključ
     * @param value  vrednost, iz katere se geslo izpelje
     * @param digits število znakov v geslu
     * @return Izračunano geslo
     */
    public static String generateHOTPSHA1(byte[] key, int value, int digits) throws NoSuchAlgorithmException, InvalidKeyException {
        return OneTimePasswordAlgorithm.generateOTP(key, value, digits, false, 16);
    }

    /**
     * Izračuna enkratno geslo v protokolu poziv-odziv
     *
     * @param key       ključ
     * @param challenge vrednost, ki predstavlja poziv
     * @return Vrednost odziva
     */
    public static String generateResponseHMAC256(byte[] key, String challenge) throws NoSuchAlgorithmException, InvalidKeyException {
        // Instanciraj MAC
        final Mac mac = Mac.getInstance("HmacSHA256");

        // Nalozi ključ
        mac.init(new SecretKeySpec(key, "HmacSHA256"));

        // Izračunaj značko
        final byte[] responseFull = mac.doFinal(challenge.getBytes(StandardCharsets.UTF_8));

        // naloži značko v ByteBuffer
        final ByteBuffer buff = ByteBuffer.wrap(responseFull);

        // uporabi pravilo debelega konca
        buff.order(ByteOrder.BIG_ENDIAN);

        // Preberi celo število (32 bitov) in postavi 32. bit na 0
        // (označuje predznak, mi pa želimo zgolj pozitivna števila)
        final int response = buff.getInt() & 0x7FFFFFFF;

        // Vrni 6 mestno geslo
        // Če je rezultat manj mesten, začetek podloži z ničlami
        return String.format("%06d%n", response % 1000000);
    }
}