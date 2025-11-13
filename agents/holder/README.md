# Mobile Wallet Implementation Guide (LEGACY REFERENCE)
# Aries Bifold/Credo Integration for Holder Agent

> **⚠️ NOTE**: This project has moved to a **web-based wallet** architecture using React + Aries Framework JavaScript.  
> See `frontend/web/WEB_WALLET_PLAN.md` for the current implementation plan.  
> This file is preserved as a reference for potential future mobile development.

This directory contains documentation and mock implementation for holder agent functionality.

## Production Implementation: Aries Bifold Mobile Wallet

The **actual holder agent** in production is a **React Native mobile application** using:

### Core Technologies
- **Aries Framework JavaScript (AFJ) / Credo**: TypeScript/JavaScript framework for Aries protocols
- **Aries Bifold**: BC Government's open-source mobile wallet built on Credo
- **React Native**: Cross-platform mobile development (iOS + Android)
- **Indy SDK / Aries Askar**: Cryptographic operations and wallet management

### Security Features
- **TEE/Secure Element**: 
  - Android: Android Keystore for hardware-backed keys
  - iOS: Secure Enclave for private key storage
- **AES-256 Wallet Encryption**: All credentials encrypted at rest
- **BIP-39 Mnemonic Recovery**: 12/24-word recovery phrase
- **Biometric Authentication**: Face ID / Touch ID / Fingerprint
- **PIN Protection**: Secondary authentication layer

### Key Components

#### 1. Aries Credo Agent Setup
```typescript
import { Agent, InitConfig } from '@aries-framework/core'
import { agentDependencies } from '@aries-framework/react-native'
import { AskarModule } from '@aries-framework/askar'
import { IndyVdrRegisterModule } from '@aries-framework/indy-vdr'
import { AnonCredsModule } from '@aries-framework/anon-creds'

const config: InitConfig = {
  label: 'User Mobile Wallet',
  walletConfig: {
    id: 'user-wallet',
    key: '<secure-key>', // Stored in Secure Enclave/Keystore
  },
}

const agent = new Agent({
  config,
  dependencies: agentDependencies,
  modules: {
    askar: new AskarModule(),
    indyVdr: new IndyVdrRegisterModule(),
    anoncreds: new AnonCredsModule(),
  },
})

await agent.initialize()
```

#### 2. DIDComm Connection Handling
```typescript
// Scan QR code from issuer/verifier
const invitation = await agent.oob.parseInvitation(qrCodeData)

// Accept invitation
const { connectionRecord } = await agent.oob.receiveInvitation(invitation)

// Wait for connection to be active
await agent.connections.returnWhenIsConnected(connectionRecord.id)
```

#### 3. Credential Reception
```typescript
// Listen for credential offers
agent.events.on(CredentialEventTypes.CredentialStateChanged, async (event) => {
  if (event.payload.credentialRecord.state === CredentialState.OfferReceived) {
    const credentialRecord = event.payload.credentialRecord
    
    // Show user credential details
    displayCredentialOffer(credentialRecord.credentialAttributes)
    
    // User accepts
    await agent.credentials.acceptOffer({
      credentialRecordId: credentialRecord.id,
    })
  }
  
  if (event.payload.credentialRecord.state === CredentialState.Done) {
    // Credential stored in encrypted wallet
    notifyUser('Credential received and stored securely')
  }
})
```

#### 4. Proof Presentation (Zero-Knowledge)
```typescript
// Listen for proof requests
agent.events.on(ProofEventTypes.ProofStateChanged, async (event) => {
  if (event.payload.proofRecord.state === ProofState.RequestReceived) {
    const proofRecord = event.payload.proofRecord
    
    // Get credentials that satisfy the proof request
    const credentials = await agent.proofs.getRequestedCredentialsForProofRequest({
      proofRecordId: proofRecord.id,
    })
    
    // User selects which attributes to reveal (selective disclosure)
    const requestedCredentials = await userSelectsCredentials(credentials)
    
    // Generate zero-knowledge proof
    await agent.proofs.acceptRequest({
      proofRecordId: proofRecord.id,
      proofFormats: {
        indy: requestedCredentials,
      },
    })
  }
})
```

#### 5. Secure Key Storage (Android)
```typescript
import * as Keychain from 'react-native-keychain'
import { Platform } from 'react-native'

// Store wallet key in Android Keystore
const storeWalletKey = async (walletKey: string) => {
  await Keychain.setGenericPassword('wallet', walletKey, {
    accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_ANY,
    accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED,
    securityLevel: Keychain.SECURITY_LEVEL.SECURE_HARDWARE,
  })
}

// Retrieve wallet key
const getWalletKey = async () => {
  const credentials = await Keychain.getGenericPassword({
    authenticationPrompt: {
      title: 'Authenticate to unlock wallet',
    },
  })
  
  if (credentials) {
    return credentials.password
  }
  throw new Error('Wallet key not found')
}
```

#### 6. BIP-39 Mnemonic Backup
```typescript
import * as bip39 from 'bip39'

// Generate recovery phrase during wallet creation
const generateMnemonic = () => {
  return bip39.generateMnemonic(256) // 24 words
}

// Restore wallet from mnemonic
const restoreWallet = async (mnemonic: string) => {
  if (!bip39.validateMnemonic(mnemonic)) {
    throw new Error('Invalid recovery phrase')
  }
  
  const seed = await bip39.mnemonicToSeed(mnemonic)
  const walletKey = deriveWalletKey(seed)
  
  await agent.wallet.initialize({
    id: 'user-wallet',
    key: walletKey,
  })
}
```

### Architecture Diagram
```
┌─────────────────────────────────────────────────┐
│         React Native Mobile App                 │
│  ┌─────────────────────────────────────────┐   │
│  │  UI Layer (Aries Bifold)                │   │
│  │  - QR Scanner                            │   │
│  │  - Credential Viewer                     │   │
│  │  - Proof Request Handler                 │   │
│  └──────────────┬──────────────────────────┘   │
│                 │                                │
│  ┌──────────────▼──────────────────────────┐   │
│  │  Aries Credo Agent (AFJ)                │   │
│  │  - DIDComm Protocol                      │   │
│  │  - Credential Exchange                   │   │
│  │  - Proof Protocol                        │   │
│  └──────────────┬──────────────────────────┘   │
│                 │                                │
│  ┌──────────────▼──────────────────────────┐   │
│  │  Aries Askar (Wallet)                   │   │
│  │  - AES-256 Encryption                    │   │
│  │  - Credential Storage                    │   │
│  │  - Key Management                        │   │
│  └──────────────┬──────────────────────────┘   │
│                 │                                │
│  ┌──────────────▼──────────────────────────┐   │
│  │  Secure Element / TEE                    │   │
│  │  - Private Key Storage (Hardware)        │   │
│  │  - Android Keystore / iOS Secure Enclave│   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### File Structure
```
frontend/mobile/
├── src/
│   ├── agent/
│   │   ├── agent.ts              # Credo agent initialization
│   │   ├── connection.ts         # Connection management
│   │   ├── credentials.ts        # Credential handling
│   │   └── proofs.ts             # Proof protocol
│   ├── security/
│   │   ├── keychain.ts           # Secure key storage
│   │   ├── biometric.ts          # Biometric authentication
│   │   └── mnemonic.ts           # BIP-39 recovery
│   ├── screens/
│   │   ├── Home.tsx
│   │   ├── QRScanner.tsx
│   │   ├── Credentials.tsx
│   │   ├── CredentialDetail.tsx
│   │   └── ProofRequest.tsx
│   └── App.tsx
├── android/                       # Android-specific native code
├── ios/                           # iOS-specific native code
├── package.json
└── README.md
```

### Dependencies
```json
{
  "dependencies": {
    "@aries-framework/core": "^0.5.0",
    "@aries-framework/react-native": "^0.5.0",
    "@aries-framework/askar": "^0.5.0",
    "@aries-framework/indy-vdr": "^0.5.0",
    "@aries-framework/anon-creds": "^0.5.0",
    "react-native": "^0.72.0",
    "react-native-keychain": "^8.1.0",
    "react-native-camera": "^4.2.0",
    "bip39": "^3.1.0"
  }
}
```

## Development Mock (This Directory)

This directory contains a **mock ACA-Py holder agent** for backend testing only. 
It simulates holder behavior during development but **is NOT used in production**.

### Mock vs Production

| Feature | Mock (ACA-Py) | Production (Aries Bifold) |
|---------|---------------|---------------------------|
| Platform | Docker Container | iOS/Android Mobile App |
| Language | Python | TypeScript (React Native) |
| Framework | Hyperledger ACA-Py | Aries Credo (AFJ) |
| UI | REST API Only | Full Mobile UI |
| Security | Basic Wallet | TEE/Secure Enclave |
| Usage | Backend Testing | End-user Production |

## Next Steps

1. **Sprint 3**: Implement React Native mobile wallet using Aries Bifold
2. **Sprint 4**: Integrate Android Keystore and iOS Secure Enclave
3. **Sprint 5**: Add BIP-39 mnemonic backup and recovery
4. **Sprint 6**: Implement IPFS document handling in mobile app

## References

- [Aries Bifold Repository](https://github.com/hyperledger/aries-mobile-agent-react-native)
- [Aries Credo Documentation](https://credo.js.org/)
- [Aries RFC 0036: Issue Credential](https://github.com/hyperledger/aries-rfcs/tree/main/features/0036-issue-credential)
- [Aries RFC 0037: Present Proof](https://github.com/hyperledger/aries-rfcs/tree/main/features/0037-present-proof)
