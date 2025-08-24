CREATE MIGRATION m1garaxt3miep4nynbtqjmpzadu7tj6ovydm2bjcr6f37lbj3japrq
    ONTO initial
{
  CREATE FUTURE simple_scoping;
  CREATE TYPE default::Source {
      CREATE REQUIRED PROPERTY type: std::str {
          CREATE CONSTRAINT std::one_of('youtube', 'rss', 'podcast', 'substack', 'bluesky');
      };
      CREATE INDEX ON (.type);
      CREATE PROPERTY is_active: std::bool {
          SET default := true;
      };
      CREATE INDEX ON (.is_active);
      CREATE PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY updated_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY url: std::str;
  };
  CREATE TYPE default::Content {
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE INDEX std::fts::index ON (std::fts::with_options(((.title ++ ' ') ++ .description), language := std::fts::Language.por));
      CREATE REQUIRED LINK source: default::Source;
      CREATE PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY duration: std::duration;
      CREATE PROPERTY published_at: std::datetime;
      CREATE PROPERTY transcript: std::str;
      CREATE PROPERTY url: std::str;
  };
  CREATE TYPE default::User {
      CREATE PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY password_hash: std::str;
      CREATE REQUIRED PROPERTY username: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
