import { issuerClient, handleApiError } from './client';

// Types
export interface Schema {
  schema_id: string;
  name: string;
  version: string;
  attributes: string[];
  created_at?: string;
}

export interface CredentialDefinition {
  cred_def_id: string;
  schema_id: string;
  tag: string;
  created_at?: string;
}

export interface IssueCredentialRequest {
  connection_id: string;
  cred_def_id: string;
  attributes: Record<string, string>;
  comment?: string;
}

export interface CredentialExchange {
  credential_exchange_id: string;
  connection_id: string;
  state: string;
  cred_def_id?: string;
  schema_id?: string;
  credential_proposal?: any;
  credential_offer?: any;
  credential?: any;
  created_at?: string;
  updated_at?: string;
}

// Issuer API functions
export const issuerApi = {
  /**
   * Get all schemas
   */
  async getSchemas(): Promise<Schema[]> {
    try {
      const response = await issuerClient.get('/schemas');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Create a new schema
   */
  async createSchema(data: {
    name: string;
    version: string;
    attributes: string[];
  }): Promise<Schema> {
    try {
      const response = await issuerClient.post('/schemas', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific schema
   */
  async getSchema(schemaId: string): Promise<Schema> {
    try {
      const response = await issuerClient.get(`/schemas/${schemaId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all credential definitions
   */
  async getCredentialDefinitions(): Promise<CredentialDefinition[]> {
    try {
      const response = await issuerClient.get('/credential-definitions');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Create a new credential definition
   */
  async createCredentialDefinition(data: {
    schema_id: string;
    tag: string;
  }): Promise<CredentialDefinition> {
    try {
      const response = await issuerClient.post('/credential-definitions', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific credential definition
   */
  async getCredentialDefinition(credDefId: string): Promise<CredentialDefinition> {
    try {
      const response = await issuerClient.get(`/credential-definitions/${credDefId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Issue a credential
   */
  async issueCredential(data: IssueCredentialRequest): Promise<CredentialExchange> {
    try {
      const response = await issuerClient.post('/credentials/issue', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get all credential exchanges
   */
  async getCredentialExchanges(): Promise<CredentialExchange[]> {
    try {
      const response = await issuerClient.get('/credentials');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * Get a specific credential exchange
   */
  async getCredentialExchange(exchangeId: string): Promise<CredentialExchange> {
    try {
      const response = await issuerClient.get(`/credentials/${exchangeId}`);
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
      const response = await issuerClient.get('/connections');
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
      const response = await issuerClient.post('/connections/create-invitation', data);
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
      const response = await issuerClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
