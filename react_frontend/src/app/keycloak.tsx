import Keycloak from "keycloak-js";


// Setup Keycloak instance
export const keycloak = new Keycloak({
  url: "http://localhost:7080",
  realm: "BrokerX",
  clientId: "react-brokerX",
});
