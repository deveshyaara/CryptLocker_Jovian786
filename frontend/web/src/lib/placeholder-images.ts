/**
 * Placeholder Images for the Application
 * Using placeholder.com for demo images
 */

export interface PlaceholderImage {
  id: string;
  imageUrl: string;
  alt: string;
}

export const PlaceHolderImages: PlaceholderImage[] = [
  {
    id: 'user-avatar-1',
    imageUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
    alt: 'User Avatar',
  },
  {
    id: 'user-avatar-2',
    imageUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
    alt: 'User Avatar',
  },
  {
    id: 'credential-badge',
    imageUrl: 'https://via.placeholder.com/150/4F46E5/FFFFFF?text=Credential',
    alt: 'Credential Badge',
  },
  {
    id: 'connection-badge',
    imageUrl: 'https://via.placeholder.com/150/10B981/FFFFFF?text=Connection',
    alt: 'Connection Badge',
  },
  {
    id: 'proof-badge',
    imageUrl: 'https://via.placeholder.com/150/F59E0B/FFFFFF?text=Proof',
    alt: 'Proof Badge',
  },
];
