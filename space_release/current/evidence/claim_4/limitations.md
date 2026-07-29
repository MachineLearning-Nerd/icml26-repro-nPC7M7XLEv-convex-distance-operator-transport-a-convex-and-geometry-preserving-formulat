# Claim 4 limitations and deviations

- The complete first-100/all-4,950-pair protocol tests the Table 3 numerical
  cells and directions. It does not recover unpublished original filenames,
  code, or seeds.
- No node is padded, relabeled, or replaced. Consequently, the invalid subject
  cannot enter a 170-by-170 matching evaluation without changing the primary
  data.
- The first 100 lexical subjects are unaffected by the sole invalid subject,
  which occurs later in the archive order.
- The paper does not specify whether its diffusion Laplacian is normalized.
  The main route pins the normalized choice rather than silently guessing.
- Directional recovery and exact-cell recovery are reported separately.
- Both method directions reproduce, but diffusion CDOT differs from the paper
  by about `+0.1050` absolute. Unpublished preprocessing details prevent
  claiming exact-cell recovery.
- The data provider calls the archive Scale 2 / 170 nodes; the verifier checks
  the stronger condition that every archived session has exact atlas IDs
  1 through 170.
