import Keycloak from "keycloak-js";

export const keycloak = new Keycloak({
  url: "http://localhost:8080",
  realm: "BrokerX",
  clientId: "react-brokerX",
});
