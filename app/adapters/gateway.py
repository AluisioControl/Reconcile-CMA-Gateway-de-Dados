class GatewayAdapter:
    """Adapter para converter dados do gateway para o novo formato."""

    @staticmethod
    def parse_gateway_data(data_gateway):
        """
        Converte os campos do gateway para o novo formato especificado.

        Args:
            data_gateway (dict): Dicionário com os dados originais do gateway

        Returns:
            dict: Dicionário com os campos convertidos
        """
        parsed_data = {
            "id_gtw": data_gateway.get("id", None),
            "name_gtw": data_gateway.get("name", None),
            "ip_gtw": data_gateway.get("ip", None),
            "active_gtw": data_gateway.get("active", None),
            "id_sub": data_gateway.get("substation", {}).get("id", None),
            "name_sub": data_gateway.get("substation", {}).get("name", None),
            "active_sub": data_gateway.get("substation", {}).get("active", None),
            "sapAbbreviation_sub": data_gateway.get("substation", {}).get("sapAbbreviation", None),
            "createdAt_gtw": data_gateway.get("createdAt", None),
            "updatedAt_gtw": data_gateway.get("updatedAt", None),
            "userCreatedId_gtw": data_gateway.get("userCreatedId", None),
            "userUpdatedId_gtw": data_gateway.get("userUpdatedId", None),
            "substationId_gtw": data_gateway.get("substationId", None)
        }
        return parsed_data