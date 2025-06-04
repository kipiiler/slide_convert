# Slide Conversion Examples

This directory contains sample conversions from the CSE 484 Computer Security course, demonstrating the capabilities of the slide conversion tool.

## Featured Lectures

- **Lecture 11**: Public Key Encryption + Digital Signatures
- **Lecture 17**: CSRF and XSS Review  
- **Lecture 18**: Web Security Fundamentals
- **Lecture 19**: Privacy and Web Tracking

## Conversion Output Structure

Each lecture conversion includes:

```
lectureName.pdf/
├── full.md              # Complete extracted content
├── captioned.md         # Content with AI-generated image descriptions  
├── images/              # Extracted images with hash-based names
├── layout.json          # Detailed layout analysis
├── *_content_list.json  # Structured content metadata
└── *_origin.pdf         # Original PDF file
```

### Lecture 11 - Cryptography Concepts
```markdown
# RSA Cryptosystem [Rivest, Shamir, Adleman 1977]

Operates over $Z_{n}^{\star}$ for n = pq (product of 2 primes)

Key generation:
- Generate large primes p, q
- Compute $n = pq$ and $\varphi(n) = (p-1)(q-1)$
- Choose small e, relatively prime to φ(n)
- Compute modular inverse d: ed = 1 mod φ(n)

Encryption: ct = m^e mod n
Decryption: ct^d mod n = (m^e)^d mod n = m
```

### Lecture 17 - Web Security
```markdown
# CSRF Defenses

- Double-submit magic token in POST (and the cookie)
- Origin headers/referer checking
- Cookie restrictions (SameSite)
- Validate what the browser says about request originating from

![Diagram illustrating a cross-site request forgery (CSRF) attack where an attacker's website tricks a user's browser into sending a legitimate request to a bank](images/example.jpg)
```

## File Formats

### `full.md`
Raw extraction without image captions - fastest processing, essential content only.

### `captioned.md` 
Enhanced version with AI-generated image descriptions for accessibility and better understanding.

### `images/`
Contains all extracted images as JPEG files with SHA-256 hash names for uniqueness.

### `layout.json`
Technical metadata about document structure, positioning, and analysis results.


*Generated using the Slide Converter tool with MinerU API and Google Gemini for image captioning.* 