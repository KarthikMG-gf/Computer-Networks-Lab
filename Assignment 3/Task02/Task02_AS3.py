"""Q2: TCP congestion window over 20 round trips: slow start, avoidance and loss."""

def simulate(losses, ssthresh=16, reno=True):
    cwnd, trace = 1, []
    for rtt in range(1, 21):
        trace.append(cwnd)
        # TODO 1: If this RTT is in losses: set ssthresh = max(cwnd // 2, 2) and set
        #   cwnd to ssthresh (Reno, fast recovery) or to 1 (Tahoe). Otherwise double
        #   cwnd in slow start (cwnd < ssthresh, capped at ssthresh) or add 1 in
        #   congestion avoidance
        if rtt in losses:
            ssthresh = max(cwnd // 2, 2)
            cwnd = ssthresh if reno else 1
        else:
            if cwnd < ssthresh:
                cwnd = min(cwnd * 2, ssthresh)
            else:
                cwnd += 1
    return trace

if __name__ == "__main__":
    results = {}
    for label, reno in (("Reno ", True), ("Tahoe", False)):
        tr = simulate({8, 14}, reno=reno)
        results[label.strip()] = tr
        print(label, " ".join(f"{w:2d}" for w in tr), f"| segments sent {sum(tr)}")

    extra = sum(results["Reno"]) - sum(results["Tahoe"])
    print(f"Extra segments delivered by Reno over Tahoe: {extra}")

    # Optional plotting if matplotlib is installed
    try:
        import matplotlib.pyplot as plt
        rtts = list(range(1, 21))
        plt.figure(figsize=(8, 4))
        plt.plot(rtts, results["Reno"], marker="o", label="TCP Reno (211 segs)")
        plt.plot(rtts, results["Tahoe"], marker="s", linestyle="--", label="TCP Tahoe (144 segs)")
        plt.xlabel("Round-Trip Time (RTT)")
        plt.ylabel("Congestion Window (cwnd in MSS)")
        plt.title("TCP Reno vs. TCP Tahoe Congestion Window (Losses at RTT 8 & 14)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig("q2_cwnd_plot.png", dpi=150)
        print("Saved plot to q2_cwnd_plot.png")
    except ImportError:
        pass
