from services.model_wrappers.base_model_remote import APIModel
from typing import Optional, List
from utils.config import get_hf_key

import openai


class APIModelHuggingFace(APIModel):
    """
    A wrapper class for interacting with HuggingFace models using TGI
    (https://github.com/huggingface/text-generation-inference). TGI implements
    the OpenAI API for HuggingFace models.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3000/v1",
        name: Optional[str] = "huggingface_tgi_model",
        description: Optional[str] = "TGI model wrapper",
    ) -> None:
        """
        Initializes a HuggingFace model using TGI with the given name and description.
        """
        super().__init__(name=name, description=description)
        self.hf_token = get_hf_key()
        self.client = openai.OpenAI(base_url=base_url, api_key=self.hf_token)

    def _model_predict(self, inputs: List[str]) -> List[str]:
        """
        Sends preprocessed inputs to HuggingFace model and retrieves responses.

        Args:
            inputs (List[str]): A list of preprocessed input strings.

        Returns:
            List[str]: A list of responses from the HuggingFace model.
        """

        responses = []
        for input_text in inputs:
            try:
                # response = self.client.chat.completions.create(
                #     messages=[
                #         # {"role": "system", "content": "You are a helpful assistant."},
                #         {"role": "user", "content": input_text},
                #     ],
                #     model="gpt-3.5-turbo",
                #     max_tokens=150,
                #     temperature=0.7,
                # )
                # responses.append(response.choices[0].message.content)

                response = self.client.chat.completions.create(
                    model="tgi",
                    messages=[
                        # {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": input_text},
                    ],
                    stream=False,
                )
                responses.append(response)
            except Exception as e:
                responses.append(f"Error: {str(e)}")

        return responses
