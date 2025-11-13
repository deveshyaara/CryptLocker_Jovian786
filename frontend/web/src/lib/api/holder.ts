import { holderClient, handleApiError } from './client';

// Types
export interface Wallet {
  owner_did: string;
  agent_url: string;
  created_at?: string;
}

export interface Connection {
  connection_id: string;
  state: string;
  their_label?: string;
  their_did?: string;
  my_did?: string;
  invitation_key?: string;
  invitation_url?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Credential {
  credential_id: string;
  schema_id?: string;
  cred_def_id?: string;
  state: string;
  credential_proposal?: any;
  credential_offer?: any;
  credential?: any;
  attributes?: Record<string, string>;
  created_at?: string;
  updated_at?: string;
}

export interface Proof {
  presentation_exchange_id: string;
  state: string;
  verified?: string;
  presentation?: any;
  presentation_request?: any;
  created_at?: string;
  updated_at?: string;
}

export interface CreateInvitationRequest {
  alias?: string;
  auto_accept?: boolean;
  multi_use?: boolean;
}

export interface ReceiveInvitationRequest {
  invitation_url: string;
  alias?: string;
  auto_accept?: boolean;
}

export interface SendProofRequest {
  connection_id: string;
  proof_request: any;
}

// Holder API functions
export const holderApi = {
  /**
   * Get wallet DID information
   */
  async getWallet(token?: string): Promise<{ did: string; wallet_id: string; owner_did?: string }> {
    try {
      const config = token ? {
        headers: { Authorization: `Bearer ${token}` }
      } : {};
      const response = await holderClient.get('/wallet/did', config);
      // Map 'did' to 'owner_did' for backwards compatibility
      const data = response.data;
      return {
        ...data,
        owner_did: data.did || data.owner_did
      };
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Create a new invitation
   */
  async createInvitation(data: CreateInvitationRequest = {}): Promise<Connection> {
    try {
      const response = await holderClient.post('/connections/create-invitation', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Receive an invitation
   */
  async receiveInvitation(data: ReceiveInvitationRequest): Promise<Connection> {
    try {
      const response = await holderClient.post('/connections/receive-invitation', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all connections
   */
  async getConnections(): Promise<Connection[]> {
    try {
      const response = await holderClient.get('/connections');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific connection
   */
  async getConnection(connectionId: string): Promise<Connection> {
    try {
      const response = await holderClient.get(`/connections/${connectionId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Accept a connection request
   */
  async acceptConnection(connectionId: string): Promise<Connection> {
    try {
      const response = await holderClient.post(`/connections/${connectionId}/accept`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Delete a connection
   */
  async deleteConnection(connectionId: string): Promise<void> {
    try {
      await holderClient.delete(`/connections/${connectionId}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all credentials
   */
  async getCredentials(): Promise<Credential[]> {
    try {
      const response = await holderClient.get('/credentials');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific credential
   */
  async getCredential(credentialId: string): Promise<Credential> {
    try {
      const response = await holderClient.get(`/credentials/${credentialId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Accept a credential offer
   */
  async acceptCredential(credentialId: string): Promise<Credential> {
    try {
      const response = await holderClient.post(`/credentials/${credentialId}/accept`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Reject a credential offer
   */
  async rejectCredential(credentialId: string): Promise<void> {
    try {
      await holderClient.post(`/credentials/${credentialId}/reject`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Delete a credential
   */
  async deleteCredential(credentialId: string): Promise<void> {
    try {
      await holderClient.delete(`/credentials/${credentialId}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all proofs/presentations
   */
  async getProofs(): Promise<Proof[]> {
    try {
      const response = await holderClient.get('/proofs');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific proof
   */
  async getProof(proofId: string): Promise<Proof> {
    try {
      const response = await holderClient.get(`/proofs/${proofId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Send a proof presentation
   */
  async sendProof(proofId: string, presentation: any): Promise<Proof> {
    try {
      const response = await holderClient.post(`/proofs/${proofId}/send`, { presentation });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get health status
   */
  async getHealth(): Promise<{ status: string }> {
    try {
      const response = await holderClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
