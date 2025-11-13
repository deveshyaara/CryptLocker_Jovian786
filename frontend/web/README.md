# CryptLocker Web Wallet - Frontend

A modern, decentralized identity web wallet built with Next.js 14, TypeScript, and Tailwind CSS. This frontend connects to the CryptLocker backend SSI (Self-Sovereign Identity) system powered by Hyperledger Aries.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Wallet Management**: Manage DIDs and verifiable credentials
- **Connection Management**: Establish connections with issuers and verifiers
- **Credential Management**: Receive, store, and present credentials
- **Proof Requests**: Handle and respond to proof requests
- **Real-time Updates**: Live dashboard with actual backend data
- **Protected Routes**: Automatic authentication checks
- **Responsive Design**: Mobile-first UI with Tailwind CSS
- **Type Safety**: Full TypeScript support

## 📋 Prerequisites

- Node.js 18+ and npm 9+
- Backend services running (Holder, Issuer, Verifier agents)
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Development Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend/web
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` with your backend API URLs:
   ```env
   NEXT_PUBLIC_HOLDER_API_URL=http://localhost:8031
   NEXT_PUBLIC_ISSUER_API_URL=http://localhost:8030
   NEXT_PUBLIC_VERIFIER_API_URL=http://localhost:8032
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
npm start
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

From the project root:

```bash
docker-compose up -d frontend-web
```

This will:
- Build the frontend image
- Start the frontend service
- Connect to backend services
- Expose on port 3000

### Standalone Docker Build

```bash
cd frontend/web
docker build -t cryptlocker-frontend .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_HOLDER_API_URL=http://holder-agent:8031 \
  cryptlocker-frontend
```

## 📁 Project Structure

```
frontend/web/
├── src/
│   ├── app/                    # Next.js 14 App Router
│   │   ├── dashboard/          # Protected dashboard pages
│   │   ├── login/              # Login page
│   │   ├── register/           # Registration page
│   │   ├── layout.tsx          # Root layout with AuthProvider
│   │   └── page.tsx            # Landing page
│   ├── components/
│   │   ├── auth/               # Authentication components
│   │   │   └── protected-route.tsx
│   │   ├── common/             # Shared components
│   │   │   ├── app-header.tsx
│   │   │   ├── app-sidebar.tsx
│   │   │   └── logo.tsx
│   │   └── ui/                 # UI components (shadcn/ui)
│   ├── lib/
│   │   ├── api/                # API service layer
│   │   │   ├── client.ts       # Axios client with interceptors
│   │   │   ├── auth.ts         # Authentication API
│   │   │   ├── credentials.ts  # Credentials API
│   │   │   ├── connections.ts  # Connections API
│   │   │   ├── proofs.ts       # Proofs API
│   │   │   ├── wallet.ts       # Wallet API
│   │   │   └── index.ts
│   │   ├── contexts/
│   │   │   └── auth-context.tsx  # Auth context provider
│   │   ├── types/
│   │   │   └── api.ts          # TypeScript type definitions
│   │   ├── config.ts           # Environment configuration
│   │   └── utils.ts            # Utility functions
│   └── hooks/
│       ├── use-toast.ts        # Toast notifications hook
│       └── use-mobile.tsx      # Mobile detection hook
├── public/                     # Static assets
├── .env.local                  # Environment variables (local)
├── .env.example                # Environment template
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
├── package.json                # Dependencies
└── Dockerfile                  # Docker build file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_HOLDER_API_URL` | Holder agent API endpoint | `http://localhost:8031` |
| `NEXT_PUBLIC_ISSUER_API_URL` | Issuer agent API endpoint | `http://localhost:8030` |
| `NEXT_PUBLIC_VERIFIER_API_URL` | Verifier agent API endpoint | `http://localhost:8032` |
| `NEXT_PUBLIC_API_URL` | Default API endpoint | `http://localhost:8031` |
| `NEXT_PUBLIC_WS_URL` | WebSocket endpoint | `ws://localhost:8031` |

### API Client Configuration

The API client (`src/lib/api/client.ts`) includes:
- Automatic JWT token management
- Request/response interceptors
- Error handling and formatting
- 401 redirect to login
- Token storage in localStorage

## 🔐 Authentication Flow

1. **Registration** (`/register`)
   - User submits registration form
   - Backend creates user and DID
   - JWT token returned and stored
   - Redirect to dashboard

2. **Login** (`/login`)
   - User submits credentials
   - Backend validates and returns JWT
   - Token stored in localStorage
   - Redirect to dashboard

3. **Protected Routes**
   - Dashboard wrapped in `ProtectedRoute` component
   - Checks authentication on mount
   - Redirects to login if not authenticated
   - Shows loading state during check

4. **Logout**
   - Clears token from storage
   - Redirects to login page

## 📡 API Integration

### Authentication Service
```typescript
import { authService } from '@/lib/api';

// Register
await authService.register({
  username: 'john_doe',
  email: 'john@example.com',
  password: 'securepass',
  full_name: 'John Doe'
});

// Login
await authService.login({
  username: 'john_doe',
  password: 'securepass'
});

// Get current user
const user = await authService.getCurrentUser();
```

### Credentials Service
```typescript
import { credentialsService } from '@/lib/api';

// Get all credentials
const credentials = await credentialsService.getCredentials();

// Get credential by ID
const credential = await credentialsService.getCredentialById(id);

// Accept credential offer
await credentialsService.acceptCredentialOffer(exchangeId);
```

### Connections Service
```typescript
import { connectionsService } from '@/lib/api';

// Create invitation
const invitation = await connectionsService.createInvitation();

// Get all connections
const connections = await connectionsService.getConnections();
```

## 🎨 UI Components

Built with [shadcn/ui](https://ui.shadcn.com/) components:
- Button, Card, Dialog, Form
- Input, Label, Checkbox
- Toast notifications
- Sidebar, Header
- Table, Badge
- And more...

## 🧪 Testing

```bash
# Run type check
npm run type-check

# Run linter
npm run lint

# Build for production (tests build)
npm run build
```

## 🚀 Deployment

### Vercel (Recommended for Frontend)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Docker Production

```bash
# Build production image
docker build -t cryptlocker-web:prod .

# Run container
docker run -d \
  -p 3000:3000 \
  -e NEXT_PUBLIC_HOLDER_API_URL=https://api.yourdomain.com \
  --name cryptlocker-web \
  cryptlocker-web:prod
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify backend services are running
   - Check environment variables in `.env.local`
   - Ensure CORS is configured on backend

2. **Authentication Not Working**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify backend auth endpoints

3. **Build Errors**
   - Delete `node_modules` and `.next`
   - Run `npm install` again
   - Check Node.js version (18+)

4. **Type Errors**
   - Run `npm run type-check`
   - Update `@types/*` packages
   - Check `tsconfig.json` settings

## 📝 Development Guidelines

### Code Style
- Use TypeScript for all files
- Follow ESLint rules
- Use Prettier for formatting
- Component naming: PascalCase
- File naming: kebab-case

### State Management
- Use React Context for global state
- useState for local component state
- Custom hooks for reusable logic

### API Calls
- Always use API service layer
- Handle errors with try-catch
- Show loading states
- Display error messages

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

See main project LICENSE file.

## 🆘 Support

For issues and questions:
- Check documentation
- Review backend API docs
- Open GitHub issue
- Contact development team
