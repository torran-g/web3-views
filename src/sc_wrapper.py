import re
import types


class BaseContractView:
    def __init__(
        self, contract, transaction=None, block_identifier=None, ccip_read_enabled=None
    ):
        self._contract = contract
        self._caller = self._contract.caller(
            transaction, block_identifier, ccip_read_enabled
        )

    def __call__(
        self, transaction=None, block_identifier=None, ccip_read_enabled=None
    ) -> "BaseContractView":
        transaction = transaction or {}
        return type(self)(
            self._contract,
            transaction=transaction,
            block_identifier=block_identifier,
            ccip_read_enabled=ccip_read_enabled,
        )

    def __iter__(self):
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue
            if isinstance(getattr(self, attr_name), types.MethodType):
                continue
            yield attr_name, getattr(self, attr_name)

    @staticmethod
    def _make_attr(name, is_method):
        if is_method:  # if there are inputs, make it a method, otherwise a property
            return lambda self, *args, **kwargs: getattr(self._caller, name)(
                *args, **kwargs
            )
        return property(lambda self: getattr(self._caller, name)())

    @classmethod
    def _get_attr_name(cls, name, is_method, drop_get, snake):
        if not is_method and drop_get:
            name = cls._drop_get(name)
        if snake:
            name = cls._to_snake_case(name)
        return name

    @staticmethod
    def _to_snake_case(input_string):
        # Convert camel case to snake case
        snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", input_string)
        # Convert spaces and hyphens to underscores
        snake_case = re.sub("[-\s]", "_", snake_case)
        # Remove any non-alphanumeric characters except underscores
        snake_case = re.sub("[^a-zA-Z0-9_]", "", snake_case)
        # Convert to lowercase
        return snake_case.lower()

    @staticmethod
    def _drop_get(name):
        return name[3:] if name.startswith("get") else name


def view(
    contract,
    *,
    drop_get=True,
    snake=True,
    transaction=None,
    block_identifier=None,
    ccip_read_enabled=None
):
    class CustomContractView(BaseContractView):
        def __new__(cls, contract, *args, **kwargs):
            for fn in contract.all_functions():
                if fn.abi["stateMutability"] != "view":
                    continue
                is_method = bool(fn.abi["inputs"])
                attr_name = cls._get_attr_name(fn.fn_name, is_method, drop_get, snake)
                attr = cls._make_attr(fn.fn_name, is_method)
                setattr(cls, attr_name, attr)
            return super().__new__(cls)

    return CustomContractView(
        contract, transaction, block_identifier, ccip_read_enabled
    )
