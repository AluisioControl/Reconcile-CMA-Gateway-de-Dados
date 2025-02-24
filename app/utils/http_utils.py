from typing import Any, Dict, Optional

import aiohttp
import asyncio

async def fetch_with_retry(
    url: str,
    headers: Dict[str, str],
    method: str = "GET",
    max_attempts: int = 3,
    timeout: Optional[float] = 15,
    **kwargs,
) -> Any:
    """
    Faz uma requisição HTTP com retentativas em caso de timeout.

    Args:
        url (str): URL do endpoint.
        headers (Dict[str, str]): Cabeçalhos da requisição.
        method (str): Método HTTP (padrão: "GET").
        max_attempts (int): Número máximo de tentativas (padrão: 3).
        timeout (Optional[float]): Tempo limite em segundos por tentativa (opcional).
        **kwargs: Argumentos adicionais para aiohttp (ex.: json, data).

    Returns:
        Any: Resposta da requisição (JSON por padrão).

    Raises:
        Exception: Se todas as tentativas falharem ou o status não for 200.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    if response.status == 401:
                        from app.settings import configs

                        configs.relogin()
                        raise Exception(
                            "Falha na autenticação. Verifique o token de acesso."
                        )
                    raise Exception(
                        f"Falha na requisição. Código de status: {response.status}"
                    )
        except aiohttp.ClientConnectionError as e:
            print(f"Tentativa {attempt}: erro de conexão ({e}), tentando novamente...")
            if attempt == max_attempts:
                raise Exception(f"Falha após {max_attempts} tentativas: {str(e)}")
        except asyncio.exceptions.TimeoutError:
            print(f"Tentativa {attempt}: timeout, tentando novamente...")
            if attempt == max_attempts:
                raise Exception(f"Timeout persistente após {max_attempts} tentativas")
