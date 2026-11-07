"""
hashtable.py - A reusable hash table using Open Addressing with Linear Probing.

The class is generic: it stores any (key, value) pair and knows nothing about
pharmacies or medicines, so it can be reused in other programs.

Slot structure (one Python list, `self.table`):
    None          -> empty slot (never used; stops a search)
    DELETED       -> tombstone (record removed; search must keep probing past it)
    (key, value)  -> occupied slot
"""

DELETED = object()   # unique tombstone marker, can never equal a real record


def _is_prime(n):
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def _next_prime(n):
    while not _is_prime(n):
        n += 1
    return n


class HashTable:
    def __init__(self, size=7, max_load_factor=0.75, auto_resize=True):
        self.size = size
        self.table = [None] * size
        self.count = 0                 # number of live records
        self.tombstones = 0            # number of DELETED markers
        self.max_load_factor = max_load_factor
        self.auto_resize = auto_resize

    # ---------------------------------------------------------------- basics
    def hash_function(self, key):
        """Initial index = hash(key) MOD table size (works for int/str keys)."""
        return hash(key) % self.size

    @property
    def load_factor(self):
        return self.count / self.size

    def __len__(self):
        return self.count

    # ---------------------------------------------------------------- insert
    def insert(self, key, value):
        """Insert or update a record. Returns the slot index used,
        or None if the table is full (only possible with auto_resize=False)."""
        if self.auto_resize and \
                (self.count + self.tombstones + 1) / self.size > self.max_load_factor:
            self._resize()
        return self._place(key, value)

    def _place(self, key, value):
        index = self.hash_function(key)
        first_deleted = None            # first tombstone seen on the probe path

        for i in range(self.size):
            position = (index + i) % self.size      # wrap around the table end
            slot = self.table[position]

            if slot is None:                        # key is not in the table
                target = position if first_deleted is None else first_deleted
                return self._store(target, key, value)
            if slot is DELETED:
                if first_deleted is None:
                    first_deleted = position        # remember it for reuse
            elif slot[0] == key:                    # key exists -> update
                self.table[position] = (key, value)
                return position

        if first_deleted is not None:               # no empty slot, reuse tombstone
            return self._store(first_deleted, key, value)
        return None                                 # table completely full

    def _store(self, position, key, value):
        if self.table[position] is DELETED:
            self.tombstones -= 1
        self.table[position] = (key, value)
        self.count += 1
        return position

    # ---------------------------------------------------------------- search
    def _find(self, key):
        """Return (position or None, number of slots probed)."""
        index = self.hash_function(key)
        probes = 0
        for i in range(self.size):
            position = (index + i) % self.size
            slot = self.table[position]
            probes += 1
            if slot is None:
                return None, probes                 # empty slot: key absent
            if slot is not DELETED and slot[0] == key:
                return position, probes
        return None, probes

    def search(self, key):
        """Return the value stored for key, or None."""
        position, _ = self._find(key)
        return None if position is None else self.table[position][1]

    def search_with_probes(self, key):
        """Like search() but also returns how many slots were examined."""
        position, probes = self._find(key)
        value = None if position is None else self.table[position][1]
        return value, probes

    # ---------------------------------------------------------------- delete
    def delete(self, key):
        """Mark the record as DELETED (tombstone). Returns True if it existed."""
        position, _ = self._find(key)
        if position is None:
            return False
        self.table[position] = DELETED
        self.count -= 1
        self.tombstones += 1
        return True

    # ---------------------------------------------------------------- resize
    def _resize(self):
        """Grow to the next prime >= 2*size and rehash every live record.
        Tombstones are discarded during rehashing."""
        old_table = self.table
        self.size = _next_prime(self.size * 2)
        self.table = [None] * self.size
        self.count = 0
        self.tombstones = 0
        for slot in old_table:
            if slot is not None and slot is not DELETED:
                self._place(slot[0], slot[1])
