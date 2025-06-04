# CSE 484/ CSE M 584: Public Key Encryption + Digital Signatures  

Winter 2025  

Nirvan Tyagi tyagi@cs  

UW Instruction Team: David Kohlbrenner, Yoshi Kohno, Franziska Roesner, and Nirvan Tyagi. Thanks to Dan Boneh, Dieter Gollmann, Dan Halperin, John Manferdelli, John Mitchell, Vitaly Shmatikov, Bennet Yee, Nickolai Zeldovich and many others.  

# Announcements  

Things due Homework 2: Next Wednesday  

# Applications of Public Key Cryptography  

Encryption for confidentiality   
Digital signatures for integrity   
Session key establishment / "Key exchange"  

# Public Key Encryption  

![](images/31b6b9f508216d7f544c1d81a6257740adde69e88cd1f80fdbaaa4c357bff728.jpg)  

# Public Key Encryption  

![](images/e689d5261fe6cb0ee3a228950ce856d2183c8c5e6dbd0953cbfdaa2cabb451ae.jpg)  

$$
\mathsf { E n c r y p t } ( \mathsf { p k } _ { \mathsf { _ B } } , \mathsf { m } ) \to \mathsf { c t }
$$  

# Public Key Encryption  

![](images/9325d8bee15ca1cf50f2ed2d521e14b0c511fbe4dda60ab6afbcae84392fe2af.jpg)  

$\mathsf { E n c r y p t } ( \mathsf { p k } _ { \mathsf { _ B } } , \mathsf { m } ) \to \mathsf { c t }$ $\mathsf { D e c r y p t } ( \mathsf { s k } _ { \mathsf { _ B } } , \mathsf { c t } ) \to \mathsf { m }$  

# Public Key Encryption from Diffie-Hellman  

![](images/0e18bc2d3146dbb20c7865136b637e0ae0ee8746e37cdea192287a9b22c24cbd.jpg)  

# Public Key Encryption from Diffie-Hellman  

![](images/f81e8498fcf0727c4ffb0f68c4de455a84f65c76221832de7f89e0f511930dd7.jpg)  

Compute DH shared secret:   
K= H(gy)   
Encrypt with authenticated symmetric encryption:   
ctse =SE.Enc(K, m)  

# Public Key Encryption from Diffie-Hellman  

![](images/0c33e700ded3093f9fc4ef6b6f0281467e2773dfe8f769cc020facc2c5816c5e.jpg)  

# Public Key Encryption from Diffie-Hellman  

![](images/9ca497dfec97f57771dc01e4bfff3935f1d30dfb8a4ec19c08d16f1414bbed71.jpg)  

# Digital Signatures  

No one should be able to forge signatures from Bob's public key without Bob's secret key  

![](images/2347f417c9a1a3b7301e32442a9841ebbb21946b5c530c4ff4b66f4c5b4c8c65.jpg)  

# Digital Signatures  

No one should be able to forge signatures from Bob's public key without Bob's secret key  

![](images/a1acdf85fb45bc9bc4f5e783a998c8cca2245b1204e70c4f7875a8b0107c90c9.jpg)  

# Digital Signatures  

No one should be able to forge signatures from Bob's public key without Bob's secret key  

![](images/9b34e55e3dcdad45778a1b2614336f75d0c12a6c96f808c2810da7e72ea02bc8.jpg)  

# Digital Signatures  

No one should be able to forge signatures from. Bob's public key without Bob's secret key  

![](images/302b1efa9286eeea69d697c050d2f32688b913b43d7ba8e582da49d06d33f7b8.jpg)  

$\mathsf { V e r i f y } ( \mathsf { p k } _ { \mathsf { B } } , \mathsf { m } , \sigma ) \to 0 / 1$ $\mathsf { S i g n } ( \mathsf { s k } _ { \mathsf { s } } , \mathsf { m } ) \to \sigma$  

In-Class Activity 2/5: What benefit do signatures have over MACs?  

Assume prime-order group  

# Schnorr Signature  

Sample one-time key:   
r, g   
Compute random challenge:   
c=H(g',g,m)   
Prove "knowledge" of y:   
z =r+ yc  

![](images/54bce46acfc8866e6878d025027596d577bd9308beed4a7a1860de40e3c07552.jpg)  

Alice  

Assume prime-order group  

# Schnorr Signature  

Sample one-time key:   
r, g   
Compute random challenge:   
c =H(g',g,m)   
Prove "knowledge" of y:   
z =r+ yc  

![](images/5fb06db0e29ef437f3628ee8e68565bcd7b6b3c33ffe59e6dd1a3017593f75fb.jpg)  

Assume prime-order group  

# Schnorr Signature  

Sample one-time key:   
r,g   
Compute random challenge:   
c=H(g',g,m)   
Prove "knowledge" of y:   
z =r+ yc  

$$
\mathsf { \Lambda } \mathsf { c } = \mathsf { H } ( \mathrm { \Lambda } )
$$  

$$
\mathbf { g } ^ { z } = \vec { \mathbf { \nabla } } \mathbf { g } ^ { \mathsf { r } } \oplus ( \mathbf { g } ^ { \mathsf { y } } ) ^ { \mathsf { c } }
$$  

![](images/2251ac76190a7730cd9fad5a914a8d025741798a44a4ffa35021732347ce61ce.jpg)  

# RSA Cryptosystem [Rivest, Shamir, Adleman 1977]  

. Operates over $Z _ { n } ^ { \star }$ for n = pq (product of 2 primes)  

.Background: Helpful number theory facts about Z \* $- \mathrm { O r d e r } = \varphi ( \mathsf { n } ) = ( \mathsf { p } - 1 ) ( \mathsf { q } - 1 )$ . $\varphi ( { \mathfrak { n } } )$ : Euler's Totient Function: # of integers in [1,n) relatively prime to n -Euler's Theorem: $\textsf { F o r e v e r y a } \in \mathsf { Z } _ { \mathsf { n } } ^ { \star } , \mathsf { a } ^ { \varphi ( \mathsf { n } ) } = 1 \left( \mathsf { m o d } \mathsf { n } \right)$  

# RSA Cryptosystem [Rivest, Shamir, Adleman 1977]  

![](images/c5d94e4aa6bf1f19d846e2bb8eac2e58cdf7a99b338568bd58bf2667746aaf0d.jpg)  

# Key generation:  

Generate large primes p, q   
- Compute $n = p 9$ and $\scriptstyle { \varphi ( { \mathsf { n } } ) = ( { \mathsf { p } } - 1 ) ( { \mathsf { q } } - 1 ) }$   
- Choose small e, relatively prime to o(n)   
- Compute modular inverse d: ed = 1 mod $\varphi ( \mathsf { n } )$   
$- \mathrm {  ~ p k _ { \scriptscriptstyle B } = ( e , n ) } ;$  

# RSA Cryptosystem [Rivest, Shamir, Adleman 1977]  

![](images/cddebe1ac61eecbf6d1ddaf67e8a3622295c195d4ddff6bcbd76103bb9389fd7.jpg)  

# Key generation:  

- Generate large primes p, q   
Compute $n = p 9$ and $\scriptstyle \varphi ( { \mathsf { n } } ) = ( { \mathsf { p } } - 1 ) ( { \mathsf { q } } - 1 )$   
Choose small e, relatively prime to $\varphi ( { \mathsf n } )$   
- Compute modular inverse d: ed = 1 mod $\varphi ( \mathsf { n } )$   
$- \mathrm { \bf ~ p k } _ { \mathrm { \scriptscriptstyle B } } = ( \mathrm { e } , \mathrm { n } ) ;$  

Encryption: ct = me mod n  

Decryption: ctd mod n = (me)d mod n = m  

# Why is RSA Secure?  

.RSA problem: given c, n=pq, and $\mathsf { e }$ such that gcd(e, (n))=1, find m such that $\cdot$ mod n   
. Factoring problem: given positive integer n, find primes $\mathsf { p } _ { 1 } , \ldots , \mathsf { p } _ { \mathsf { k } }$ such that $\mathsf { n } { = } \mathsf { p } _ { 1 } ^ { \ \mathsf { e } _ { 1 } } \mathsf { p } _ { 2 } ^ { \ \mathsf { e } _ { 2 } } { \ldots } \mathsf { p } _ { \mathsf { k } } ^ { \mathsf { \Gamma } }$ %   
If factoring is easy, then RSA problem is easy (knowing factors means you can compute ${ \sf d } =$ inverse of e mod (p-1)(q-1))  

# Why is RSA Secure?  

. RSA problem: given c, n=pq, and $\mathsf { e }$ such that gcd(e, (n))=1, find m such that $\cdot$ mod n  

: Factoring problem: given positive integer n, find primes $\mathsf { p } _ { 1 } , \ldots , \mathsf { p } _ { \mathsf { k } }$ such that $\mathsf { n } { = } \mathsf { p } _ { 1 } ^ { \ \mathsf { e } _ { 1 } } \mathsf { p } _ { 2 } ^ { \ \mathsf { e } _ { 2 } } { \ldots } \mathsf { p } _ { \mathsf { k } } ^ { \mathsf { \Gamma } }$ ek 6  

If factoring is easy, then RSA problem is easy (knowing factors means you can compute ${ \sf d } =$ inverse of e mod (p-1)(q-1))  

Other RSA Caveats  

If m is small, can brute force   
Not randomized!   
Requires n \~ 2048-4096 bits for 128-bits of security   
Largely being phased out for efficient elliptic curve group cryptography  

# What do Quantum Computers mean for Cryptography?  

# What do Quantum Computers mean for Cryptography?  

1. Implications for existing cryptography  

# What do Quantum Computers mean for Cryptography?  

1. Implications for existing cryptography  

.Quantum algorithms exist to solve "hard" assumptions quickly o Shor's algorithm can solve factoring and discrete logarithm "Post-quantum" cryptography o  Build asymmetric cryptography for classical computers based on assumptions that we think are "hard"' even for quantum computers "Lattice-based" cryptography 2. Implications for future cryptography Quantum computing offers new hardness assumptions and new functionality from which to build cryptography  