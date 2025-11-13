import { verifierClient, handleApiError } from './client';

// Types
export interface ProofRequest {
  name: string;
  version: string;
  requested_attributes: Record<string, {
    name: string;
    restrictions?: any[];
  }>;
  requested_predicates?: Record<string, any>;
}

export interface PresentationExchange {
  presentation_exchange_id: string;
  connection_id?: string;
  state: string;
  verified?: string;
  presentation?: any;
  presentation_request?: any;
  created_at?: string;
  updated_at?: string;
}

export interface SendProofRequestData {
  connection_id: string;
  proof_request: ProofRequest;
  comment?: string;
}

// Verifier API functions
export const verifierApi = {
  /**
   * Send a proof request
   */
  async sendProofRequest(data: SendProofRequestData): Promise<PresentationExchange> {
    try {
      const response = await verifierClient.post('/proofs/request', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all presentation exchanges
   */
  async getPresentationExchanges(): Promise<PresentationExchange[]> {
    try {
      const response = await verifierClient.get('/proofs');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific presentation exchange
   */
  async getPresentationExchange(exchangeId: string): Promise<PresentationExchange> {
    try {
      const response = await verifierClient.get(`/proofs/${exchangeId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Verify a presentation
   */
  async verifyPresentation(exchangeId: string): Promise<PresentationExchange> {
    try {
      const response = await verifierClient.post(`/proofs/${exchangeId}/verify`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all connections
   */
  async getConnections(): Promise<any[]> {
    try {
      const response = await verifierClient.get('/connections');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Create an invitation
   */
  async createInvitation(data: {
    alias?: string;
    auto_accept?: boolean;
    multi_use?: boolean;
  } = {}): Promise<any> {
    try {
      const response = await verifierClient.post('/connections/create-invitation', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Receive an invitation
   */
  async receiveInvitation(data: {
    invitation_url: string;
    alias?: string;
    auto_accept?: boolean;
  }): Promise<any> {
    try {
      const response = await verifierClient.post('/connections/receive-invitation', data);
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
      const response = await verifierClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
