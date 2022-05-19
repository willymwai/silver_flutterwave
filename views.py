from silver.payment_processors import get_instance
from silver.payment_processors.views import GenericTransactionView
from django.conf import settings
import requests
from urllib.parse import urlencode
import stripe
from money.money import Money
from money.currency import Currency


class FlutterWaveTransactionView(GenericTransactionView):
    @staticmethod
    def get_stripe_client_secret(transaction):
        """Get the Stripe client secret for the transaction."""
        _ = "https://api.stripe.com/v1/payment_intents"
        amount = transaction.invoice.total
        currency = transaction.invoice.currency
        smallest_amount_unit = Money(amount, getattr(Currency, currency)).sub_units
        payload = {
            "amount": smallest_amount_unit,
            "currency": currency,
            "automatic_payment_methods[enabled]": True,
        }
        print("================================")
        stripe.api_key = "sk_test_51Kt455AVsErfOrz55mgK3KAoDEchHD1N3sREGSV3lK7vyJ0E5WQc5m14h0lZxBb6IffGYXBl2uGhwJugSzu5LjNY00OWBuPk4M"
        intent_response = stripe.PaymentIntent.create(**payload)
        print("********************************************")
        print(intent_response)
        return intent_response.get("client_secret")

    def get_context_data(self):
        context_data = super(FlutterWaveTransactionView, self).get_context_data()
        payment_processor = get_instance(self.transaction.payment_processor)
        context_data["client_token"] = payment_processor.client_token(
            self.transaction.customer
        )
        context_data["is_recurring"] = payment_processor.is_payment_method_recurring(
            self.transaction.payment_method
        )

        context_data["client_secret"] = self.get_stripe_client_secret(self.transaction)
        return context_data
