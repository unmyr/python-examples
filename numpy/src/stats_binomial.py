# -*- coding: utf-8 -*-
"""numpy example."""

import numpy as np


def main():
    """Run main."""
    ans = np.random.binomial(n=1000, p=0.5)
    print(ans)  # 結果を表示


if __name__ == "__main__":
    main()

# EOF
