import { holderApi } from './holder';

/**
 * Credentials Service - Helper functions for credential operations
 */
export const credentialsService = {
  /**
   * Get total count of credentials
   */
  async getCredentialsCount(): Promise<number> {
    try {
      const credentials = await holderApi.getCredentials();
      return credentials.length;
    } catch (error) {
      console.error('Failed to get credentials count:', error);
      return 0;
    }
  },

  /**
   * Get credentials by state
   */
  async getCredentialsByState(state: string) {
    try {
      const credentials = await holderApi.getCredentials();
      return credentials.filter((cred) => cred.state === state);
    } catch (error) {
      console.error('Failed to get credentials by state:', error);
      return [];
    }
  },

  /**
   * Get active (issued) credentials
   */
  async getActiveCredentials() {
    return this.getCredentialsByState('credential_issued');
  },
};

/**
 * Connections Service - Helper functions for connection operations
 */
export const connectionsService = {
  /**
   * Get count of active connections
   */
  async getActiveConnectionsCount(): Promise<number> {
    try {
      const connections = await holderApi.getConnections();
      const activeConnections = connections.filter(
        (conn) => conn.state === 'active' || conn.state === 'completed'
      );
      return activeConnections.length;
    } catch (error) {
      console.error('Failed to get active connections count:', error);
      return 0;
    }
  },

  /**
   * Get connections by state
   */
  async getConnectionsByState(state: string) {
    try {
      const connections = await holderApi.getConnections();
      return connections.filter((conn) => conn.state === state);
    } catch (error) {
      console.error('Failed to get connections by state:', error);
      return [];
    }
  },

  /**
   * Get all active connections
   */
  async getActiveConnections() {
    try {
      const connections = await holderApi.getConnections();
      return connections.filter(
        (conn) => conn.state === 'active' || conn.state === 'completed'
      );
    } catch (error) {
      console.error('Failed to get active connections:', error);
      return [];
    }
  },
};

/**
 * Proofs Service - Helper functions for proof operations
 */
export const proofsService = {
  /**
   * Get count of pending proof requests
   */
  async getPendingProofRequestsCount(): Promise<number> {
    try {
      const proofs = await holderApi.getProofs();
      const pendingProofs = proofs.filter(
        (proof) => proof.state === 'request_received' || proof.state === 'presentation_sent'
      );
      return pendingProofs.length;
    } catch (error) {
      console.error('Failed to get pending proof requests count:', error);
      return 0;
    }
  },

  /**
   * Get proofs by state
   */
  async getProofsByState(state: string) {
    try {
      const proofs = await holderApi.getProofs();
      return proofs.filter((proof) => proof.state === state);
    } catch (error) {
      console.error('Failed to get proofs by state:', error);
      return [];
    }
  },

  /**
   * Get all pending proof requests
   */
  async getPendingProofRequests() {
    try {
      const proofs = await holderApi.getProofs();
      return proofs.filter(
        (proof) => proof.state === 'request_received' || proof.state === 'presentation_sent'
      );
    } catch (error) {
      console.error('Failed to get pending proof requests:', error);
      return [];
    }
  },

  /**
   * Get all verified proofs
   */
  async getVerifiedProofs() {
    try {
      const proofs = await holderApi.getProofs();
      return proofs.filter((proof) => proof.verified === 'true');
    } catch (error) {
      console.error('Failed to get verified proofs:', error);
      return [];
    }
  },
};
