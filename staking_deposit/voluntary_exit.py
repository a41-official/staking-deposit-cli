from staking_deposit.settings import BaseChainSetting
from staking_deposit.utils.ssz import SignedVoluntaryExit, VoluntaryExit, compute_voluntary_exit_domain, \
    compute_signing_root
from py_ecc.bls import G2ProofOfPossession as bls


def generate_signed_voluntary_exit_message(chain_settings: BaseChainSetting, signing_key: int, validator_index: int, epoch: int) -> SignedVoluntaryExit:
    message = VoluntaryExit(
        epoch=epoch,
        validator_index=validator_index
    )

    domain = compute_voluntary_exit_domain(
        fork_version=chain_settings.EXIT_FORK_VERSION,
        genesis_validators_root=chain_settings.GENESIS_VALIDATORS_ROOT
    )

    signing_root = compute_signing_root(message, domain)
    signature = bls.Sign(signing_key, signing_root)

    signed_msg = SignedVoluntaryExit(
        message=message,
        signature=signature
    )

    return signed_msg