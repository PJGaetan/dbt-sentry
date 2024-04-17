from dbt_sentry.options import GlobalCompareOptions, GlobalHeadOptions


class Artefact:
    def __init__(self, target: str, manifest: ):
        self.target_head = head_options.target
        self.target_compare = compare_options.target_compare
        self.manifest_head_path = head_options.manifest_path
        self.manifest_compare_path = compare_options.manifest_compare_path
