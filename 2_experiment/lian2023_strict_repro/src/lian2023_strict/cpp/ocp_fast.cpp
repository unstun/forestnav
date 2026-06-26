#include <algorithm>
#include <cmath>
#include <cstdint>
#include <limits>
#include <vector>

namespace {

constexpr int kStateDim = 5;
constexpr int kControlDim = 2;
constexpr int kDiskDim = 2;

double softplus(double x) {
    if (x >= 0.0) {
        return x + std::log1p(std::exp(-x));
    }
    return std::log1p(std::exp(x));
}

double sigmoid(double x) {
    if (x >= 0.0) {
        const double e = std::exp(-x);
        return 1.0 / (1.0 + e);
    }
    const double e = std::exp(x);
    return e / (1.0 + e);
}

inline const double& state_at(const double* states, std::int64_t k, int col) {
    return states[k * kStateDim + col];
}

inline const double& control_at(const double* controls, std::int64_t k, int col) {
    return controls[k * kControlDim + col];
}

inline const double& disk_at(const double* disks, std::int64_t k, std::int64_t j, std::int64_t disc_count, int col) {
    return disks[(k * disc_count + j) * kDiskDim + col];
}

inline double& grad_state_at(double* grad_states, std::int64_t k, int col) {
    return grad_states[k * kStateDim + col];
}

inline double& grad_control_at(double* grad_controls, std::int64_t k, int col) {
    return grad_controls[k * kControlDim + col];
}

inline double& grad_disk_at(double* grad_disks, std::int64_t k, std::int64_t j, std::int64_t disc_count, int col) {
    return grad_disks[(k * disc_count + j) * kDiskDim + col];
}

bool valid_shape(std::int64_t state_rows, std::int64_t control_rows, std::int64_t disc_count) {
    return state_rows > 0 && control_rows >= 0 && state_rows == control_rows + 1 && disc_count > 0;
}

double local_state_constraint(
    double x,
    double y,
    double v,
    double xa,
    double xb,
    double ya,
    double yb,
    double za,
    double zb,
    double beta
) {
    const double raw_x = -((x - xa) * (x - xb));
    const double raw_y = -((y - ya) * (y - yb));
    const double fx = std::max(raw_x, 0.0);
    const double fy = std::max(raw_y, 0.0);
    const double z = std::abs(v);
    const double g = (z - za) * (z - zb);
    const double fz = softplus(beta * g) / beta;
    return fx * fy * fz;
}

}  // namespace

extern "C" {

int lian2023_formula23_penalty_value(
    const double* states,
    std::int64_t state_rows,
    const double* controls,
    std::int64_t control_rows,
    const double* disks,
    std::int64_t disc_count,
    const double* offsets,
    double tf,
    double wheelbase,
    int enable_local_state_constraint,
    double xa,
    double xb,
    double ya,
    double yb,
    double za,
    double zb,
    double beta,
    double* out_value
) {
    if (!states || !controls || !disks || !offsets || !out_value || !valid_shape(state_rows, control_rows, disc_count)) {
        return 1;
    }
    const std::int64_t n = control_rows;
    const double denom_n = static_cast<double>(std::max<std::int64_t>(n, 1));
    const double dt = tf / denom_n;
    double j3 = 0.0;
    double j7 = 0.0;
    double j15 = 0.0;

    for (std::int64_t k = 0; k < n; ++k) {
        const double x = state_at(states, k, 0);
        const double y = state_at(states, k, 1);
        const double theta = state_at(states, k, 2);
        const double v = state_at(states, k, 3);
        const double phi = state_at(states, k, 4);
        const double a = control_at(controls, k, 0);
        const double omega = control_at(controls, k, 1);
        const double residuals[5] = {
            state_at(states, k + 1, 0) - x - dt * v * std::cos(theta),
            state_at(states, k + 1, 1) - y - dt * v * std::sin(theta),
            state_at(states, k + 1, 2) - theta - dt * v * std::tan(phi) / wheelbase,
            state_at(states, k + 1, 3) - v - dt * a,
            state_at(states, k + 1, 4) - phi - dt * omega,
        };
        for (double residual : residuals) {
            j3 += residual * residual;
        }
    }

    for (std::int64_t k = 0; k < state_rows; ++k) {
        const double x = state_at(states, k, 0);
        const double y = state_at(states, k, 1);
        const double theta = state_at(states, k, 2);
        const double cos_th = std::cos(theta);
        const double sin_th = std::sin(theta);
        for (std::int64_t j = 0; j < disc_count; ++j) {
            const double expected_x = x + offsets[j] * cos_th;
            const double expected_y = y + offsets[j] * sin_th;
            const double rx = disk_at(disks, k, j, disc_count, 0) - expected_x;
            const double ry = disk_at(disks, k, j, disc_count, 1) - expected_y;
            j7 += rx * rx + ry * ry;
        }
        if (enable_local_state_constraint) {
            const double local = local_state_constraint(x, y, state_at(states, k, 3), xa, xb, ya, yb, za, zb, beta);
            j15 += local * local;
        }
    }

    *out_value = j3 + j7 + j15;
    return 0;
}

int lian2023_formula23_penalty_gradient(
    const double* states,
    std::int64_t state_rows,
    const double* controls,
    std::int64_t control_rows,
    const double* disks,
    std::int64_t disc_count,
    const double* offsets,
    double tf,
    double wheelbase,
    int enable_local_state_constraint,
    double xa,
    double xb,
    double ya,
    double yb,
    double za,
    double zb,
    double beta,
    double* grad_states,
    double* grad_controls,
    double* grad_disks,
    double* grad_tf
) {
    if (!states || !controls || !disks || !offsets || !grad_states || !grad_controls || !grad_disks || !grad_tf ||
        !valid_shape(state_rows, control_rows, disc_count)) {
        return 1;
    }
    const std::int64_t n = control_rows;
    const double denom_n = static_cast<double>(std::max<std::int64_t>(n, 1));
    const double dt = tf / denom_n;

    std::fill(grad_states, grad_states + state_rows * kStateDim, 0.0);
    std::fill(grad_controls, grad_controls + control_rows * kControlDim, 0.0);
    std::fill(grad_disks, grad_disks + state_rows * disc_count * kDiskDim, 0.0);
    *grad_tf = 0.0;

    for (std::int64_t k = 0; k < n; ++k) {
        const double x = state_at(states, k, 0);
        const double theta = state_at(states, k, 2);
        const double v = state_at(states, k, 3);
        const double phi = state_at(states, k, 4);
        const double a = control_at(controls, k, 0);
        const double omega = control_at(controls, k, 1);
        const double cos_th = std::cos(theta);
        const double sin_th = std::sin(theta);
        const double tan_phi = std::tan(phi);
        const double cos_phi = std::cos(phi);
        const double sec2_phi = 1.0 / std::max(cos_phi * cos_phi, 1e-12);
        const double residuals[5] = {
            state_at(states, k + 1, 0) - x - dt * v * cos_th,
            state_at(states, k + 1, 1) - state_at(states, k, 1) - dt * v * sin_th,
            state_at(states, k + 1, 2) - theta - dt * v * tan_phi / wheelbase,
            state_at(states, k + 1, 3) - v - dt * a,
            state_at(states, k + 1, 4) - phi - dt * omega,
        };
        const double s0 = 2.0 * residuals[0];
        grad_state_at(grad_states, k + 1, 0) += s0;
        grad_state_at(grad_states, k, 0) -= s0;
        grad_state_at(grad_states, k, 2) += s0 * dt * v * sin_th;
        grad_state_at(grad_states, k, 3) -= s0 * dt * cos_th;
        *grad_tf -= s0 * (v * cos_th / denom_n);

        const double s1 = 2.0 * residuals[1];
        grad_state_at(grad_states, k + 1, 1) += s1;
        grad_state_at(grad_states, k, 1) -= s1;
        grad_state_at(grad_states, k, 2) -= s1 * dt * v * cos_th;
        grad_state_at(grad_states, k, 3) -= s1 * dt * sin_th;
        *grad_tf -= s1 * (v * sin_th / denom_n);

        const double s2 = 2.0 * residuals[2];
        grad_state_at(grad_states, k + 1, 2) += s2;
        grad_state_at(grad_states, k, 2) -= s2;
        grad_state_at(grad_states, k, 3) -= s2 * dt * tan_phi / wheelbase;
        grad_state_at(grad_states, k, 4) -= s2 * dt * v * sec2_phi / wheelbase;
        *grad_tf -= s2 * (v * tan_phi / (denom_n * wheelbase));

        const double s3 = 2.0 * residuals[3];
        grad_state_at(grad_states, k + 1, 3) += s3;
        grad_state_at(grad_states, k, 3) -= s3;
        grad_control_at(grad_controls, k, 0) -= s3 * dt;
        *grad_tf -= s3 * (a / denom_n);

        const double s4 = 2.0 * residuals[4];
        grad_state_at(grad_states, k + 1, 4) += s4;
        grad_state_at(grad_states, k, 4) -= s4;
        grad_control_at(grad_controls, k, 1) -= s4 * dt;
        *grad_tf -= s4 * (omega / denom_n);
    }

    for (std::int64_t k = 0; k < state_rows; ++k) {
        const double x = state_at(states, k, 0);
        const double y = state_at(states, k, 1);
        const double theta = state_at(states, k, 2);
        const double cos_th = std::cos(theta);
        const double sin_th = std::sin(theta);
        for (std::int64_t j = 0; j < disc_count; ++j) {
            const double offset = offsets[j];
            const double expected_x = x + offset * cos_th;
            const double expected_y = y + offset * sin_th;
            const double rx = disk_at(disks, k, j, disc_count, 0) - expected_x;
            const double ry = disk_at(disks, k, j, disc_count, 1) - expected_y;
            grad_disk_at(grad_disks, k, j, disc_count, 0) += 2.0 * rx;
            grad_disk_at(grad_disks, k, j, disc_count, 1) += 2.0 * ry;
            grad_state_at(grad_states, k, 0) -= 2.0 * rx;
            grad_state_at(grad_states, k, 1) -= 2.0 * ry;
            grad_state_at(grad_states, k, 2) += 2.0 * offset * rx * sin_th;
            grad_state_at(grad_states, k, 2) -= 2.0 * offset * ry * cos_th;
        }
    }

    if (enable_local_state_constraint) {
        for (std::int64_t k = 0; k < state_rows; ++k) {
            const double x = state_at(states, k, 0);
            const double y = state_at(states, k, 1);
            const double v = state_at(states, k, 3);
            const double raw_x = -((x - xa) * (x - xb));
            const double raw_y = -((y - ya) * (y - yb));
            const double fx = std::max(raw_x, 0.0);
            const double fy = std::max(raw_y, 0.0);
            if (fx <= 0.0 || fy <= 0.0) {
                continue;
            }
            const double z = std::abs(v);
            const double g = (z - za) * (z - zb);
            const double bz = beta * g;
            const double fz = softplus(bz) / beta;
            const double sig = sigmoid(bz);
            const double local = fx * fy * fz;
            const double scale = 2.0 * local;
            grad_state_at(grad_states, k, 0) += scale * (xa + xb - 2.0 * x) * fy * fz;
            grad_state_at(grad_states, k, 1) += scale * fx * (ya + yb - 2.0 * y) * fz;
            if (v != 0.0) {
                const double dz_dv = v > 0.0 ? 1.0 : -1.0;
                const double dfz_dv = sig * (2.0 * z - za - zb) * dz_dv;
                grad_state_at(grad_states, k, 3) += scale * fx * fy * dfz_dv;
            }
        }
    }

    return 0;
}

int lian2023_packed_objective(
    const double* q,
    std::int64_t control_rows,
    std::int64_t disc_count,
    const double* offsets,
    double penalty_weight,
    double mu1,
    double mu2,
    double mu3,
    double wheelbase,
    int enable_local_state_constraint,
    double xa,
    double xb,
    double ya,
    double yb,
    double za,
    double zb,
    double beta,
    double* out_value
) {
    if (!q || !offsets || !out_value || control_rows < 0 || disc_count <= 0) {
        return 1;
    }
    const std::int64_t state_rows = control_rows + 1;
    const std::int64_t state_len = state_rows * kStateDim;
    const std::int64_t control_len = control_rows * kControlDim;
    const std::int64_t disk_len = state_rows * disc_count * kDiskDim;
    const double* states = q;
    const double* controls = q + state_len;
    const double* disks = q + state_len + control_len;
    const double tf = q[state_len + control_len + disk_len];

    double objective16 = mu1 * tf;
    for (std::int64_t k = 0; k < control_rows; ++k) {
        const double dv = state_at(states, k + 1, 3) - state_at(states, k, 3);
        const double dphi = state_at(states, k + 1, 4) - state_at(states, k, 4);
        objective16 += mu2 * dv * dv + mu3 * dphi * dphi;
    }

    double penalty = 0.0;
    const int rc = lian2023_formula23_penalty_value(
        states,
        state_rows,
        controls,
        control_rows,
        disks,
        disc_count,
        offsets,
        tf,
        wheelbase,
        enable_local_state_constraint,
        xa,
        xb,
        ya,
        yb,
        za,
        zb,
        beta,
        &penalty
    );
    if (rc != 0) {
        return rc;
    }
    *out_value = objective16 + penalty_weight * penalty;
    return 0;
}

int lian2023_packed_gradient(
    const double* q,
    std::int64_t control_rows,
    std::int64_t disc_count,
    const double* offsets,
    double penalty_weight,
    double mu1,
    double mu2,
    double mu3,
    double wheelbase,
    int enable_local_state_constraint,
    double xa,
    double xb,
    double ya,
    double yb,
    double za,
    double zb,
    double beta,
    double* out_gradient
) {
    if (!q || !offsets || !out_gradient || control_rows < 0 || disc_count <= 0) {
        return 1;
    }
    const std::int64_t state_rows = control_rows + 1;
    const std::int64_t state_len = state_rows * kStateDim;
    const std::int64_t control_len = control_rows * kControlDim;
    const std::int64_t disk_len = state_rows * disc_count * kDiskDim;
    const std::int64_t total_len = state_len + control_len + disk_len + 1;
    const double* states = q;
    const double* controls = q + state_len;
    const double* disks = q + state_len + control_len;
    const double tf = q[state_len + control_len + disk_len];

    std::fill(out_gradient, out_gradient + total_len, 0.0);
    double* out_states = out_gradient;
    double* out_controls = out_gradient + state_len;
    double* out_disks = out_gradient + state_len + control_len;
    double* out_tf = out_gradient + state_len + control_len + disk_len;

    for (std::int64_t k = 0; k < control_rows; ++k) {
        const double dv = state_at(states, k + 1, 3) - state_at(states, k, 3);
        const double dphi = state_at(states, k + 1, 4) - state_at(states, k, 4);
        grad_state_at(out_states, k, 3) -= 2.0 * mu2 * dv;
        grad_state_at(out_states, k + 1, 3) += 2.0 * mu2 * dv;
        grad_state_at(out_states, k, 4) -= 2.0 * mu3 * dphi;
        grad_state_at(out_states, k + 1, 4) += 2.0 * mu3 * dphi;
    }
    *out_tf = mu1;

    std::vector<double> grad_states(static_cast<std::size_t>(state_len), 0.0);
    std::vector<double> grad_controls(static_cast<std::size_t>(control_len), 0.0);
    std::vector<double> grad_disks(static_cast<std::size_t>(disk_len), 0.0);
    double grad_tf = 0.0;
    const int rc = lian2023_formula23_penalty_gradient(
        states,
        state_rows,
        controls,
        control_rows,
        disks,
        disc_count,
        offsets,
        tf,
        wheelbase,
        enable_local_state_constraint,
        xa,
        xb,
        ya,
        yb,
        za,
        zb,
        beta,
        grad_states.data(),
        grad_controls.data(),
        grad_disks.data(),
        &grad_tf
    );
    if (rc != 0) {
        return rc;
    }
    for (std::int64_t i = 0; i < state_len; ++i) {
        out_states[i] += penalty_weight * grad_states[static_cast<std::size_t>(i)];
    }
    for (std::int64_t i = 0; i < control_len; ++i) {
        out_controls[i] += penalty_weight * grad_controls[static_cast<std::size_t>(i)];
    }
    for (std::int64_t i = 0; i < disk_len; ++i) {
        out_disks[i] += penalty_weight * grad_disks[static_cast<std::size_t>(i)];
    }
    *out_tf += penalty_weight * grad_tf;
    return 0;
}

}  // extern "C"
