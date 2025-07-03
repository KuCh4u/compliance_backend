import os
import httpx

RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

async def verify_recaptcha(token: str, action_expected: str = "submit", threshold: float = 0.5) -> bool:
    if not RECAPTCHA_SECRET_KEY:
        raise ValueError("Falta la clave secreta de reCATPCHA")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": token
            }
        )

        result = response.json()
    print('result', result)
    success = result.get("success", False)
    score = result.get("score", 0)
    print(success, score, threshold)
    return success and score >= threshold