# Mobile Wallet Foundation - React Native with Aries Bifold/Credo

## Overview
This directory will contain the React Native mobile wallet application using Aries Bifold/Credo SDK for SSI wallet functionality.

## Architecture

### Technology Stack
- **React Native**: Cross-platform mobile development
- **Aries Bifold/Credo SDK**: SSI wallet capabilities
- **TypeScript**: Type-safe development
- **React Navigation**: Mobile navigation
- **Redux Toolkit**: State management
- **Secure Storage**: Native secure element integration

### Security Features
- **TEE/Secure Element Integration**:
  - Android: Android Keystore System
  - iOS: Secure Enclave
- **Biometric Authentication**: Face ID / Touch ID / Fingerprint
- **AES-256 Wallet Encryption**
- **BIP-39 Mnemonic Recovery**: 12/24-word phrase backup
- **End-to-End Encrypted DIDComm**: Secure peer-to-peer messaging

## Directory Structure (To Be Created)
```
frontend/mobile/
├── android/                    # Android native code
├── ios/                        # iOS native code
├── src/
│   ├── components/            # Reusable UI components
│   ├── screens/               # Application screens
│   │   ├── OnboardingScreen.tsx
│   │   ├── WalletScreen.tsx
│   │   ├── CredentialsScreen.tsx
│   │   ├── ScanQRScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── services/              # Business logic services
│   │   ├── WalletService.ts   # Aries Credo integration
│   │   ├── DIDService.ts      # DID management
│   │   ├── CredentialService.ts
│   │   └── BiometricService.ts
│   ├── store/                 # Redux store
│   ├── navigation/            # Navigation configuration
│   ├── utils/                 # Utility functions
│   ├── types/                 # TypeScript types
│   └── App.tsx               # Root component
├── package.json
├── tsconfig.json
└── README.md
```

## Sprint 3-4: Mobile Wallet Implementation Plan

### Phase 1: Project Setup (Hours 0-2)
- [ ] Initialize React Native project with TypeScript
- [ ] Install Aries Bifold/Credo SDK dependencies
- [ ] Configure native modules (Android Keystore, iOS Secure Enclave)
- [ ] Set up navigation and state management
- [ ] Configure secure storage

### Phase 2: Wallet Core (Hours 2-6)
- [ ] Implement wallet initialization with Aries Credo
- [ ] Create secure key generation (Ed25519 keypairs)
- [ ] Implement BIP-39 mnemonic generation and recovery
- [ ] Set up biometric authentication
- [ ] Implement wallet encryption (AES-256-GCM)

### Phase 3: DID Management (Hours 6-10)
- [ ] Create DID generation and storage
- [ ] Implement DID Document management
- [ ] Build connection establishment (DIDComm)
- [ ] QR code scanning for invitations
- [ ] Connection list and management UI

### Phase 4: Credential Management (Hours 10-16)
- [ ] Implement credential offer reception
- [ ] Build credential acceptance flow
- [ ] Create credential storage with encryption
- [ ] Design credentials list UI
- [ ] Implement credential detail view
- [ ] Add credential revocation status checking

### Phase 5: Selective Disclosure (Hours 16-20)
- [ ] Implement proof request handling
- [ ] Build attribute selection UI
- [ ] Create zero-knowledge proof generation
- [ ] Implement presentation submission
- [ ] Add predicate verification support

### Phase 6: UI/UX Polish (Hours 20-24)
- [ ] Design onboarding flow
- [ ] Create loading states and animations
- [ ] Implement error handling and user feedback
- [ ] Add accessibility features
- [ ] Build settings and backup screens

## Integration Points

### Aries Credo SDK Interface
```typescript
interface AriesCredoAgent {
  // Wallet operations
  initialize(config: AgentConfig): Promise<void>
  createWallet(mnemonic: string): Promise<Wallet>
  unlockWallet(pin: string): Promise<void>
  
  // Connection operations
  createInvitation(): Promise<OutOfBandInvitation>
  receiveInvitation(invitation: string): Promise<Connection>
  acceptConnection(connectionId: string): Promise<void>
  
  // Credential operations
  receiveCredentialOffer(offer: CredentialOffer): Promise<void>
  acceptCredentialOffer(credentialId: string): Promise<void>
  getCredentials(): Promise<Credential[]>
  
  // Presentation operations
  receivePresentationRequest(request: PresentationRequest): Promise<void>
  createPresentation(request: PresentationRequest, credentials: Credential[]): Promise<Presentation>
  submitPresentation(presentation: Presentation): Promise<void>
}
```

### Secure Storage Interface
```typescript
interface SecureStorage {
  // TEE/Secure Element operations
  generateKey(alias: string): Promise<string>
  sign(alias: string, data: Uint8Array): Promise<Uint8Array>
  encrypt(data: Uint8Array, key: string): Promise<Uint8Array>
  decrypt(data: Uint8Array, key: string): Promise<Uint8Array>
  
  // Biometric operations
  authenticateWithBiometrics(): Promise<boolean>
  isBiometricAvailable(): Promise<boolean>
}
```

## Security Considerations

### Key Storage
- **Private keys NEVER leave secure element**
- DID keypairs stored in:
  - Android: Hardware-backed Keystore (StrongBox if available)
  - iOS: Secure Enclave
- Master encryption key derived from user PIN + salt
- Wallet data encrypted at rest with AES-256-GCM

### Recovery Mechanism
- BIP-39 mnemonic phrase (12 or 24 words)
- User responsible for secure backup
- Optional encrypted cloud backup with additional passphrase
- Recovery flow rebuilds wallet from mnemonic

### Communication Security
- All DIDComm messages encrypted end-to-end
- Perfect forward secrecy with ephemeral keys
- Message authentication with HMAC
- No plaintext credential data in transit

## Next Steps

To begin mobile wallet implementation:

1. **Install React Native CLI**:
   ```bash
   npm install -g react-native-cli
   ```

2. **Initialize Project**:
   ```bash
   cd frontend/mobile
   npx react-native init CryptLockerWallet --template react-native-template-typescript
   ```

3. **Install Aries Credo**:
   ```bash
   npm install @aries-framework/core @aries-framework/react-native
   npm install @aries-framework/indy-sdk react-native-indy-sdk
   ```

4. **Configure Native Dependencies**:
   ```bash
   cd ios && pod install
   cd android && ./gradlew build
   ```

## Testing Strategy

- **Unit Tests**: Jest for business logic
- **Integration Tests**: Test wallet operations with mock agents
- **E2E Tests**: Detox for full user flows
- **Security Tests**: Penetration testing for key storage
- **Usability Tests**: User testing for onboarding and flows

## References

- [Aries Bifold Documentation](https://github.com/hyperledger/aries-mobile-agent-react-native)
- [Aries Credo Documentation](https://credo.js.org/)
- [React Native Security Best Practices](https://reactnative.dev/docs/security)
- [Android Keystore System](https://developer.android.com/training/articles/keystore)
- [iOS Secure Enclave](https://developer.apple.com/documentation/security/certificate_key_and_trust_services/keys/protecting_keys_with_the_secure_enclave)

---

**Status**: Foundation documented, ready for Sprint 3-4 implementation
**Priority**: HIGH - Core user-facing component
**Dependencies**: Issuer and Verifier agents must be operational first
