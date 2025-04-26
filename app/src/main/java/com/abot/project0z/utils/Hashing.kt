package com.abot.project0z.utils

import org.bouncycastle.crypto.digests.MD5Digest
import org.bouncycastle.util.encoders.Hex

fun hashByteArray(input: ByteArray): ByteArray {
    val digest = MD5Digest()
    digest.update(input, 0, input.size)
    val hashBytes = ByteArray(digest.digestSize)
    digest.doFinal(hashBytes, 0)
    return Hex.encode(hashBytes)
}

fun verifyByteArray(input: ByteArray, expectedHash: ByteArray): Boolean {
    val actualHash = hashByteArray(input)
    return actualHash.equals(expectedHash)
}
