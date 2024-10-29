def call_n_times_m_times(n, m):
    def decorator(func):
        def wrapper():
            for _ in range(n):
                for _ in range(m):
                    func()

        return wrapper

    return decorator


@call_n_times_m_times(2, 2)
def print_hello():
    print("Hello")
