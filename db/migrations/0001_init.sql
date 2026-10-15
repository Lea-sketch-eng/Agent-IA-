-- Schéma initial. Ajoutez vos migrations suivantes dans des fichiers
-- numérotés (0002_xxx.sql, 0003_xxx.sql…) : elles sont appliquées dans l'ordre,
-- une seule fois, automatiquement par Railway à chaque déploiement.
CREATE TABLE IF NOT EXISTS app_settings (
    key        text PRIMARY KEY,
    value      jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);
