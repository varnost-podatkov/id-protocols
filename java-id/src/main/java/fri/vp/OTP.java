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
     * Generates a time-based one-time password
     *
     * @param key      Key to be used
     * @param time     current time in unix format
     * @param interval the time interval
     * @param digits   number of digits to display the result
     * @return Computed OTP
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
     * Generates a hmac-based one-time password.
     *
     * @param key    to be used
     * @param value  the value from which the password will be computed
     * @param digits the number of digits for the OTP
     * @return Computed OTP
     */
    public static String generateHOTPSHA1(byte[] key, int value, int digits) throws NoSuchAlgorithmException, InvalidKeyException {
        return OneTimePasswordAlgorithm.generateOTP(key, value, digits, false, 16);
    }

    /**
     * Computes a one-time password in a challenge-response protocol
     *
     * @param key       to be used
     * @param challenge the challenge from the server
     * @return The response value
     */
    public static String generateResponseHMAC256(byte[] key, String challenge) throws NoSuchAlgorithmException, InvalidKeyException {
        // Instanciraj MAC
        final Mac mac = Mac.getInstance("HmacSHA256");

        // Nalozi kljuc
        mac.init(new SecretKeySpec(key, "HmacSHA256"));

        // Izracunaj znacko
        final byte[] responseFull = mac.doFinal(challenge.getBytes(StandardCharsets.UTF_8));

        // nalozi znacko
        final ByteBuffer buff = ByteBuffer.wrap(responseFull);

        // uporabi pravilo debelega konca
        buff.order(ByteOrder.BIG_ENDIAN);

        // Preberi INT in postavi 32. bit na 0 (označuje predznak in želimo zgolj pozitivna števila)
        final int response = buff.getInt() & 0x7FFFFFFF;

        // Vrni 6 mest (tudi če so na začetku ničle)
        return String.format("%06d%n", response % 1000000);
    }
}