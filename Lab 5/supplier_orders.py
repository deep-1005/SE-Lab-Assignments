"""Supplier purchase order tracker for a stores department.

Places orders with suppliers, marks deliveries as received, notifies the
warehouse and cleans up fulfilled orders.
"""
# PES1UG24CS144_Deeptha

import logging
import sqlite3

CREATE_TABLE_SQL = ("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, supplier TEXT, "
                    "item TEXT, quantity INTEGER, received INTEGER, remarks TEXT)")


class SupplierOrderTracker:
    """Keeps purchase orders in SQLite and tracks the total quantity ordered."""

    def __init__(self, db_path=":memory:"):
        """Open the database and make sure the orders table exists."""
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(CREATE_TABLE_SQL)
        self.order_total = 0

    def place_order(self, supplier, item, quantity):
        """Insert a new order and return the running total quantity ordered."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        self.conn.execute("INSERT INTO orders (supplier, item, quantity, received) "
                          "VALUES (?, ?, ?, 0)", (supplier, item, quantity))
        self.order_total+=quantity
        return self.order_total

    def mark_received(self, order_id, remarks=""):
        """Mark an order as received, store the remarks and report success."""
        cursor = self.conn.execute("UPDATE orders SET received = 1, remarks = ? WHERE id = ?",
                                   (remarks, order_id))
        return cursor.rowcount == 1

    def cleanup(self):
        """Delete received orders and return how many rows were removed."""
        try:
            cursor = self.conn.execute("DELETE FROM orders WHERE received = 1")
        except sqlite3.Error as exc:
            logging.error("Cleanup of received orders failed: %s", exc)
            return 0
        return cursor.rowcount

    def pending_count(self):
        """Return the number of orders that have not been received yet."""
        return self.conn.execute("SELECT COUNT(*) FROM orders WHERE received = 0").fetchone()[0]


def notify_warehouse(supplier):
    """Tell the warehouse about a delivery without spawning a shell."""
    print("notifying warehouse about " + supplier)


def main():
    """Run a short demonstration of the order tracker."""
    tracker = SupplierOrderTracker()
    tracker.place_order("Acme Steel", "rods", 40)
    tracker.place_order("Bolt Co", "bolts", 500)
    tracker.mark_received(1, "ok")
    notify_warehouse("Acme")
    print(tracker.pending_count(), tracker.order_total)
    tracker.cleanup()


if __name__ == "__main__":
    main()