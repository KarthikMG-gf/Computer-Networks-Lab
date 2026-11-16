"""Q5: M/M/1 model of a router output link: arrivals at rate lam, service at rate mu."""
import heapq
import random

def mm1(lam, mu):
    # TODO 1: Return the utilisation rho = lam/mu, the average number in the system L =
    #   rho/(1-rho) and the average delay W = 1/(mu-lam). Return None if lam >= mu (the
    #   queue grows without limit)
    if lam >= mu:
        return None
    rho = lam / mu
    L = rho / (1.0 - rho)
    W = 1.0 / (mu - lam)
    return rho, L, W

def simulate_fifo_vs_priority(video_rate=200, backup_rate=750, mu=1000, duration=20.0):
    """Discrete-event simulation comparing FIFO vs Strict Priority for Video."""
    random.seed(42)
    for mode in ("FIFO", "PRIORITY"):
        t = 0.0
        server_free = 0.0
        queue = []  # (priority, arrival_time, seq)
        video_delays = []
        seq = 0
        total_rate = video_rate + backup_rate
        while t < duration:
            t += random.expovariate(total_rate)
            is_video = random.random() < (video_rate / total_rate)
            prio = 0 if (mode == "PRIORITY" and is_video) else 1
            heapq.heappush(queue, (prio, t, seq, is_video))
            seq += 1
            while queue and server_free <= t:
                _, arr, _, vid = heapq.heappop(queue)
                start = max(arr, server_free)
                service = random.expovariate(mu)
                server_free = start + service
                if vid:
                    video_delays.append((server_free - arr) * 1000.0)
        avg_d = sum(video_delays) / len(video_delays)
        print(f"Mode={mode:<8} | Video Avg Delay = {avg_d:.2f} ms (at total load {total_rate} pkt/s)")

if __name__ == "__main__":
    mu = 1000  # packets per second the link can send
    for lam in (500, 800, 900, 950, 990, 1000):
        r = mm1(lam, mu)
        if r is None:
            print(f"load {lam:4d} pkt/s: unstable, queue grows without limit")
        else:
            rho, L, W = r
            print(f"load {lam:4d} pkt/s: rho {rho:.2f}  L {L:6.1f} pkts  W {W * 1000:6.1f} ms")

    # Capacity needed for W < 10 ms (0.010 s) at lam = 1500 pkt/s:
    required_mu = 1500 + (1.0 / 0.010)
    print(f"\nRequired link capacity for W < 10 ms at 1500 pkt/s: > {required_mu:.0f} pkt/s")
    simulate_fifo_vs_priority()
